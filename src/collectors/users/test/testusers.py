#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from users import UsersCollector

import sys


################################################################################


class TestUsersCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('UsersCollector', {
            'utmp': self.getFixturePath('utmp.centos6'),
        })

        self.collector = UsersCollector(config, None)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        
        # Because of the compiled nature of pyutmp, we can't actually test
        # different operating system versions then the currently running
        # one
        if sys.platform.startswith('linux'):
            self.collector.collect()
                
            metrics = {
                'kormoc':   2,
                'root':     3,
                'total':    5,
            }
    
            self.setDocExample(self.collector.__class__.__name__, metrics)
            self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()