import itertools
import logging
import os.path
import re

import product
from typing import Iterable


IMAGE_EXTENSIONS = ['.fits', '.calb', '.pass1', '.csub', '.avgs', '.avgr', '.arch']


def preflight_products(products: Iterable[product.Product]) -> Iterable[product.Product]:
    """
    Filters out products that are either technically valid, or would produce a disproportionate number of errors
    in the validator. These errors are written to the log instead.
    """
    for candidate in products:
        errors = preflight(candidate)
        if len(errors) > 0:
            message = "\n\t" + "\n\t".join(errors)
            logging.warning(f'Product {candidate.labelfilename} failed preflight: {message}')
        else:
            yield candidate


def preflight(candidate: product.Product) -> list[str]:
    """
    Performs a series of checks against each product.
    """
    return list(
        itertools.chain(
            check_date_presence(candidate),
            check_date_order(candidate),
            check_observation_area(candidate)
        )
    )


def check_date_order(candidate: product.Product) -> Iterable[str]:
    if candidate.start_date() is not None and candidate.stop_date() is not None:
        if not len(candidate.stop_date()) == len(candidate.start_date()):
            yield 'Start date and stop date are not the same precision'
        else:
            if candidate.stop_date() < candidate.start_date():
                yield 'Stop date occurs after start date'


def check_date_presence(candidate: product.Product) -> Iterable[str]:
    """
    Ensures that start date and stop date are not nil for certain observations
    """
    if date_required(candidate):
        if candidate.start_date() is None:
            yield 'Product is missing a start date'
        if candidate.stop_date() is None:
            yield 'Product is missing an end date'


def date_required(candidate: product.Product) -> bool:
    """
    Determines if a product is of a type that requires a date. Those would be non-calibration image products for now
    """
    if candidate.collection_id() == 'calibration':
        return False
    return any(is_image(datafile) for datafile in candidate.filenames())


def is_image(datafile: str) -> bool:
    """
    Determines if a product is an image
    """
    _, extension = os.path.splitext(datafile)
    return extension in IMAGE_EXTENSIONS


def check_observation_area(candidate: product.Product) -> Iterable[str]:
    """
    Checks the observation areas for nil component names and lids
    """
    for component in candidate.observing_system_components():
        if component.name is None:
            yield f'{component.type} observing system component has no name'
        if component.internal_reference and component.internal_reference.lid_reference is None:
            yield f'{component.type} observing system component has an empty lid'
