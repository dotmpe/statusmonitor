import uuid

import urwid


class StatusWidget(urwid.TreeWidget):

    def __init__(self, node):
        self.__super.__init__(node)
        self._w = urwid.AttrWrap(self._w, None)
        self.update_w()

        if 'status' in node.data and node.data['status']:
            self.expanded = True
        else:
            self.expanded = False
        self.update_expanded_icon()


    def update_w(self):
        self._w.attr = 'body'

    #def load_inner_widget(self):
    #    return urwid.BigText(self.get_display_text(),urwid.HalfBlock5x4Font())

    def get_display_text(self):
        node = self.get_node()
        tag = 'body'
        states = node.states()
        if node.label.lower() not in StatusNode.named and 'status' in node.data and not states:

            #and not node.data['states']:
            if node.data['status'] == 1:
                tag = 'erroredf'
            elif node.data['status'] > 1:
                tag = 'failedf'
        return [ ( tag, node.label ), ( 'body', '  '), ] + states


class StatusNode(urwid.ParentNode):

    def __init__(self, data={}, parent=None):
        self.data = data
        self.id = self.data['id'] = str(uuid.uuid4())
        if 'label' not in data:
            self.label = self.id
        else:
            self.label = self.data['label']
        urwid.ParentNode.__init__(self, self.label, key=self.id, parent=parent)

    def load_child_keys(self):
        keys = []
        if 'states' not in self.data:
            return keys
        for i, status in enumerate(self.data['states']):
            if status['label'].lower() in self.named:
                continue
            if 'id' not in status:
                sub = StatusNode(status, self)
                self.set_child_node(sub.id, sub)
                assert 'id' in self.data['states'][i]
            keys.append( status['id'] )
        return keys

    def load_widget(self):
        return StatusWidget(self)

    named = [ 'init', 'check', 'build', 'test', 'dist', 'pub' ]

    def states(self):
        states = {}
        if 'states' in self.data:
            for i, status in enumerate(self.data['states']):
                name = status['label'].lower()
                if name in self.named:
                    states[name] = self.flag_named_set( **status )
        states_ord = []
        for name in self.named:
            if name in states:
                states_ord.append(states[name])
        return states_ord

    def flag_named_set(self, label='', status=0, states=[]):
        return (
                ['passed', 'errored', 'failed'][status],
                label[0]
            )


def load_tree_from_yaml(fp):
    import yaml
    data = yaml.safe_load(fp)
    return StatusNode(data)



