from collections import defaultdict
from urllib.parse import urlencode, parse_qsl

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from common.tree import TreeNode
from ..utils import KubernetesTree
from .. import const


class ApplicationTreeNodeMixin:
    id: str
    name: str
    type: str
    category: str
    attrs: dict

    @staticmethod
    def create_tree_id(pid, type, v):
        i = dict(parse_qsl(pid))
        i[type] = v
        tree_id = urlencode(i)
        return tree_id

    @classmethod
    def create_choice_node(cls, c, id_, pid, tp, opened=False, counts=None,
                           show_empty=True, show_count=True):
        count = counts.get(c.value, 0)
        if count == 0 and not show_empty:
            return None
        label = c.label
        if count is not None and show_count:
            label = '{} ({})'.format(label, count)
        data = {
            'id': id_,
            'name': label,
            'title': label,
            'pId': pid,
            'isParent': bool(count),
            'open': opened,
            'iconSkin': '',
            'meta': {
                'type': tp,
                'data': {
                    'name': c.name,
                    'value': c.value
                }
            }
        }
        return TreeNode(**data)

    @classmethod
    def create_root_tree_node(cls, queryset, show_count=True):
        count = queryset.count() if show_count else None
        root_id = 'applications'
        root_name = _('Applications')
        if count is not None and show_count:
            root_name = '{} ({})'.format(root_name, count)
        node = TreeNode(**{
            'id': root_id,
            'name': root_name,
            'title': root_name,
            'pId': '',
            'isParent': True,
            'open': True,
            'iconSkin': '',
            'meta': {
                'type': 'applications_root',
            }
        })
        return node

    @classmethod
    def create_category_tree_nodes(cls, pid, counts=None, show_empty=True, show_count=True):
        nodes = []
        categories = const.AppType.category_types_mapper().keys()
        for category in categories:
            if not settings.XPACK_ENABLED and const.AppCategory.is_xpack(category):
                continue
            i = cls.create_tree_id(pid, 'category', category.value)
            node = cls.create_choice_node(
                category, i, pid=pid, tp='category',
                counts=counts, opened=False, show_empty=show_empty,
                show_count=show_count
            )
            if not node:
                continue
            nodes.append(node)
        return nodes

    @classmethod
    def create_types_tree_nodes(cls, pid, counts, show_empty=True, show_count=True):
        nodes = []
        temp_pid = pid
        type_category_mapper = const.AppType.type_category_mapper()
        types = const.AppType.type_category_mapper().keys()

        for tp in types:
            if not settings.XPACK_ENABLED and const.AppType.is_xpack(tp):
                continue
            category = type_category_mapper.get(tp)
            pid = cls.create_tree_id(pid, 'category', category.value)
            i = cls.create_tree_id(pid, 'type', tp.value)
            node = cls.create_choice_node(
                tp, i, pid, tp='type', counts=counts, opened=False,
                show_empty=show_empty, show_count=show_count
            )
            pid = temp_pid
            if not node:
                continue
            nodes.append(node)
        return nodes

    @staticmethod
    def get_tree_node_counts(queryset):
        counts = defaultdict(int)
        values = queryset.values_list('type', 'category')
        for i in values:
            tp = i[0]
            category = i[1]
            counts[tp] += 1
            counts[category] += 1
        return counts

    @classmethod
    def create_category_type_tree_nodes(cls, queryset, pid, show_empty=True, show_count=True):
        counts = cls.get_tree_node_counts(queryset)
        tree_nodes = []

        # 类别的节点
        tree_nodes += cls.create_category_tree_nodes(
            pid, counts, show_empty=show_empty,
            show_count=show_count
        )

        # 类型的节点
        tree_nodes += cls.create_types_tree_nodes(
            pid, counts, show_empty=show_empty,
            show_count=show_count
        )
        return tree_nodes

    @classmethod
    def create_tree_nodes(cls, queryset, root_node=None, show_empty=True, show_count=True):
        tree_nodes = []

        # 根节点有可能是组织名称
        if root_node is None:
            root_node = cls.create_root_tree_node(queryset, show_count=show_count)
            tree_nodes.append(root_node)

        tree_nodes += cls.create_category_type_tree_nodes(
            queryset, root_node.id, show_empty=show_empty, show_count=show_count
        )

        # 应用的节点
        for app in queryset:
            if not settings.XPACK_ENABLED and const.AppType.is_xpack(app.type):
                continue
            node = app.as_tree_node(root_node.id)
            tree_nodes.append(node)
        return tree_nodes

    def create_app_tree_pid(self, root_id):
        pid = self.create_tree_id(root_id, 'category', self.category)
        pid = self.create_tree_id(pid, 'type', self.type)
        return pid

    def as_tree_node(self, pid, k8s_as_tree=False):
        if self.type == const.AppType.k8s and k8s_as_tree:
            node = KubernetesTree(pid).as_tree_node(self)
        else:
            node = self._as_tree_node(pid)
        return node

    def _attrs_to_tree(self):
        if self.category == const.AppCategory.db:
            return self.attrs
        return {}

    def _as_tree_node(self, pid):
        icon_skin_category_mapper = {
            'remote_app': 'chrome',
            'db': 'database',
            'cloud': 'cloud'
        }
        icon_skin = icon_skin_category_mapper.get(self.category, 'file')
        pid = self.create_app_tree_pid(pid)
        node = TreeNode(**{
            'id': str(self.id),
            'name': self.name,
            'title': self.name,
            'pId': pid,
            'isParent': False,
            'open': False,
            'iconSkin': icon_skin,
            'meta': {
                'type': 'application',
                'data': {
                    'category': self.category,
                    'type': self.type,
                    'attrs': self._attrs_to_tree()
                }
            }
        })
        return node
