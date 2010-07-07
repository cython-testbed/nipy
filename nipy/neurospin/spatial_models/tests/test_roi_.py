# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Test the discrete_domain utilities.

Caveat assumes that the MNI template image is available at
in ~/.nipy/tests/data
"""

import numpy as np
from numpy.testing import assert_almost_equal
from nipy.neurospin.spatial_models.hroi import *

shape = (5, 6, 7)

def make_mroi():
    """Create a mulmtiple ROI instance
    """
    labels = np.zeros(shape)
    labels[4:,5:,6:] = 1
    labels[:2,:2,:2] = 2
    labels[:2, 5:, 6:] = 3
    labels[:2, :2, 6:] = 4
    labels[4:, :2, 6:] = 5
    labels[4:, :2, :2] = 6
    labels[4:, 5:, :2] = 7
    labels[:2, 5:, :2] = 8
    mroi = mroi_from_array(labels, affine=None)
    return mroi, labels

def test_mroi():
    """ Test basic constructio of mulitple_roi
    """
    mroi,_ = make_mroi()
    assert mroi.k==8
    assert len(mroi.coord)==8
    assert len(mroi.local_volume)==8

def test_size():
    """ Test mroi.size
    """
    mroi, labels = make_mroi()
    assert len(mroi.size)==8
    for k in range(8):
        print mroi.size, np.sum(labels==k+1)
        assert mroi.size[k]==np.sum(labels==k+1)
    
def test_mroi_feature():
    """test the basic construction of features
    """
    mroi, labels = make_mroi()
    aux = np.random.randn(*shape)
    data = [aux[labels==k] for k in range(1, 9)]
    mroi.set_feature('data', data)
    assert (mroi.features['data'][0] == data[0]).all()
    
def test_integrate():
    """ Test the integration
    """
    mroi, labels = make_mroi()
    aux = np.random.randn(*shape)
    data = [aux[labels==k] for k in range(1, 9)]
    mroi.set_feature('data', data)
    sums = mroi.integrate('data')
    for k in range(8):
        assert sums[k]==np.sum(data[k]) 

def test_representative():
    """ Test the computation of representative features
    """
    mroi, labels = make_mroi()
    aux = np.random.randn(*shape)
    data = [aux[labels==k] for k in range(1, 9)]
    mroi.set_feature('data', data)
    sums = mroi.representative_feature('data')
    for k in range(8):
        assert sums[k]==np.mean(data[k]) 

def test_from_ball():
    """Test the creation of mulitple rois from balls
    """
    dom = domain_from_array(np.ones((10, 10)))
    radii = np.array([2, 2, 2])
    positions = np.array([[3, 3], [3, 7], [7, 7]])
    mroi = mroi_from_balls(dom, positions, radii)
    assert mroi.k == 3
    assert (mroi.size == np.array([9, 9, 9])).all()
    
if __name__ == "__main__":
    import nose
    nose.run(argv=['', __file__])





