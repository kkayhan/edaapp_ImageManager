#!/usr/bin/env python3

import eda_config as ecfg
from utils import schema
from utils.node_utils import get_node
from common.constants import PLATFORM_SRL


def test_get_node_sanity():
    val_dut1 = 'dut1'
    val_dut1_cr = {
        "metadata": {
            "name": val_dut1
        },
        "spec": {
            "operatingSystem": PLATFORM_SRL,
            "version": "23.3.1",
            "onBoarded": False
        }
    }
    ecfg.test_addcr(schema.TOPOLOGY_NODE_SCHEMA, val_dut1_cr)
    assert get_node(val_dut1) is not None
    ecfg.test_clear_all()


if __name__ == '__main__':
    test_get_node_sanity()
