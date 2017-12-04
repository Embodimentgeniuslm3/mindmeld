#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_nlp
----------------------------------

Tests for NaturalLanguageProcessor module.
"""
# pylint: disable=locally-disabled,redefined-outer-name
from __future__ import unicode_literals

import os

import pytest

from mmworkbench.exceptions import ProcessorError, AllowedNlpClassesKeyError
from mmworkbench.components import NaturalLanguageProcessor

APP_NAME = 'kwik_e_mart'
APP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), APP_NAME)


@pytest.fixture
def empty_nlp():
    """Provides an empty, unbuilt processor instance"""
    return NaturalLanguageProcessor(APP_PATH)


@pytest.fixture(scope='module')
def nlp():
    """Provides an empty processor instance"""
    nlp = NaturalLanguageProcessor(APP_PATH)
    nlp.build()
    return nlp

#
# def test_instantiate():
#     """Tests creating an NLP instance"""
#     nlp = NaturalLanguageProcessor(APP_PATH)
#     assert nlp
#
#
# def test_build(empty_nlp):
#     """Tests building a processor with default config.
#
#     This is a basic sanity check to make sure there are no exceptions.
#     """
#     nlp = empty_nlp
#     nlp.build()
#
#
# def test_dump(nlp):
#     """Test dump method of nlp"""
#     nlp.dump()
#
#
# def test_early_process(empty_nlp):
#     """Tests that attempting to process a message without first loading or
#     building models will raise an exception"""
#     with pytest.raises(ProcessorError):
#         empty_nlp.process('Hello')
#
#
# @pytest.mark.skip
# def test_load(nlp):
#     """Tests loading a processor from disk"""
#     nlp.load()
#
#
# def test_process(nlp):
#     """Tests a basic call to process"""
#     response = nlp.process('Hello')
#
#     assert response == {
#         'text': 'Hello',
#         'domain': 'store_info',
#         'intent': 'greet',
#         'entities': []
#     }
#
#
# test_data_1 = [
#     (['store_info.find_nearest_store'], 'store near MG Road',
#      'store_info', 'find_nearest_store'),
#     (['store_info.find_nearest_store', 'store_info.greet'], 'hello!',
#      'store_info', 'greet'),
#     (['store_info.find_nearest_store'], 'hello!',
#      'store_info', 'find_nearest_store'),
#     (['store_info.*'], 'hello!', 'store_info', 'greet')
# ]
#
#
# @pytest.mark.parametrize("allowed_intents,query,expected_domain,expected_intent", test_data_1)
# def test_nlp_hierarchy_bias_for_user_bias(nlp, allowed_intents, query, expected_domain,
#                                           expected_intent):
#     """Tests user specified domain and intent biases"""
#     response = nlp.process(query, nlp.extract_allowed_intents(allowed_intents))
#
#     assert response == {
#         'text': query,
#         'domain': expected_domain,
#         'intent': expected_intent,
#         'entities': []
#     }
#
#
# test_data_2 = [
#     (['store_info.*', 'store_info.greet'],
#      'hello!', 'store_info', 'greet'),
#     (['store_info.find_nearest_store'], 'hello!', 'store_info',
#      'find_nearest_store'),
#     (['store_info.*'], 'hello!', 'store_info', 'greet'),
#     (['store_info.*', 'store_info.find_nearest_store'], 'store near MG Road',
#      'store_info', 'find_nearest_store')
# ]
#
#
# @pytest.mark.parametrize("allowed_intents,query,expected_domain,expected_intent", test_data_2)
# def test_nlp_hierarchy_using_domains_intents(nlp, allowed_intents,
#                                              query, expected_domain,
#                                              expected_intent):
#     """Tests user specified allowable domains and intents"""
#     response = nlp.process(query, nlp.extract_allowed_intents(allowed_intents))
#
#     assert response == {
#         'text': query,
#         'domain': expected_domain,
#         'intent': expected_intent,
#         'entities': []
#     }


test_data_3 = [
    "what mythical scottish town appears for one day every 100 years",
    "lets run 818m",
    "Get me the product id ws-c2950t-24-24 tomorrow",
    ""
]


@pytest.mark.parametrize("query", test_data_3)
def test_nlp_hierarchy_for_queries_mallard_fails_on(nlp, query):
    """Tests user specified allowable domains and intents"""
    response = nlp.process(query)
    assert response['text'] == query


def test_validate_and_extract_allowed_intents(nlp):
    """Tests user specified allowable domains and intents"""
    with pytest.raises(ValueError):
        nlp.extract_allowed_intents(['store_info'])
    with pytest.raises(AllowedNlpClassesKeyError):
        nlp.extract_allowed_intents(['unrelated_domain.*'])
    with pytest.raises(AllowedNlpClassesKeyError):
        nlp.extract_allowed_intents(['store_info.unrelated_intent'])
