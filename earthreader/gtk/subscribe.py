""":mod:`earthreader.gtk.subscribe` --- Subscription model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from gi.repository.GObject import Object
from gi.repository.Gtk import TreeIter, TreeModel, TreeModelFlags, TreePath
from libearth.stage import Stage

__all__ = 'SubscriptionTreeModel',


class SubscriptionTreeModel(Object, TreeModel):
    """

    .. seealso::

       :file:`treemodel_large.py`
          http://git.io/nspwyw

    """
 
    __gtype_name__ = 'SubscriptionTreeModel'

    def __init__(self, stage):
        if not isinstance(stage, Stage):
            raise TypeError('stage must be {0.__module__}.{0.__name__}, not '
                            '{1!r}'.format(Stage, stage))
        super(SubscriptionTreeModel, self).__init__()
        self.stage = stage
        with stage:
            # FIXME: it currently slices the list to workaround the mysterious
            # (at least for me) rendering bug of TreeView.  It seems to
            # get incorrectly rendered when there are more than about 50 items.
            self.subscriptions = list(stage.subscriptions)[:40]
        self.subscriptions.sort(key=lambda o: (o.type, o.label.lower()))

    def make_iterator(self, index=0, return_model_iterator=False):
        if return_model_iterator:
            it = TreeIter()
            it.user_data = index
            return it
        return index

    def do_get_flags(self):
        return TreeModelFlags.ITERS_PERSIST

    def do_get_n_columns(self):
        return 1

    def do_get_column_type(self, column):
        assert 0 <= column < 1
        return str

    def do_get_iter(self, path):
        index = path.get_indices()[0]
        if 0 <= index < self.iter_n_children(None):
            return True, self.make_iterator(index, return_model_iterator=True)
        return False, None

    def do_get_path(self, it):
        return TreePath([it.user_data])

    def do_get_value(self, it, column):
        assert 0 <= column < 1
        return self.subscriptions[it.user_data].label

    def do_iter_next(self, it):
        if it.user_data + 1 < self.iter_n_children(None):
            it.user_data += 1
            return True
        return False

    def do_iter_previous(self, it):
        if it.user_data > 0:
            it.user_data -= 1
            return True
        return False

    def do_iter_children(self, parent):
        if parent is None:
            # root
            return True, self.make_iterator(0, return_model_iterator=True)
        return False, None

    def do_iter_has_child(self, it):
        return it is None

    def do_iter_n_children(self, it):
        if it is None:
            return len(self.subscriptions)
        return 0

    def do_iter_nth_child(self, parent, n):
        if parent is None:
            if 0 <= n < self.iter_n_children(parent):
                return True, self.make_iterator(n, return_model_iterator=True)
            return False, None
        return False, None

    def do_iter_parent(self, child):
        return False, None
