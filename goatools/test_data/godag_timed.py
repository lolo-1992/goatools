"""Test the loading of the optional GO term fields."""
# https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html

__copyright__ = "Copyright (C) 2010-2018, DV Klopfenstein, H Tang, All rights reserved."
__author__ = "DV Klopfenstein"


import os
import sys
import timeit
import datetime
from goatools.obo_parser import GODag
from goatools.base import download_go_basic_obo


# pylint: disable=too-few-public-methods
class GoDagTimed(object):
    """Load and store GO-DAG. Report elapsed time."""

    def __init__(self, fin_obo, opt_field=None, keep_alt_ids=False):
        self.opt = opt_field  # None causes all fields to read to exp dict
        self.obo = fin_obo
        self._init_dnld_dag()
        self.go2obj = self._init_go2obj(keep_alt_ids)

    def _init_go2obj(self, keep_alt_ids):
        """GO DAG with or without alternate GO IDs."""
        go2obj = self.load_dag(self.opt)
        return go2obj if keep_alt_ids else {o.id:o for o in go2obj.values()}

    def _init_dnld_dag(self):
        """If dag does not exist, download it."""
        if not os.path.exists(self.obo):
            download_go_basic_obo(self.obo, loading_bar=None)

    def load_dag(self, opt_fields=None):
        """Run numerous tests for various self.reports."""
        tic = timeit.default_timer()
        dag = GODag(self.obo, opt_fields)
        toc = timeit.default_timer()
        msg = "Elapsed HMS for OBO DAG load: {HMS} OPTIONAL_ATTR({O})\n".format(
            HMS=str(datetime.timedelta(seconds=(toc-tic))), O=opt_fields)
        sys.stdout.write(msg)
        return dag


# Copyright (C) 2010-2018, DV Klopfenstein, H Tang, All rights reserved.
