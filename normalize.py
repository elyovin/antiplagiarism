import ast


class Normalizer(ast.NodeTransformer):
    def __init__(self):
        self.func_replacements = {}
        self.class_replacements = {}
        self.asyncfunc_replacements = {}
        self.name_replacements = {}

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._delete_annotation(node)
        self._rename_args(node)
        self._delete_docstring(node)
        self.generic_visit(node)

        new_id = self.func_replacements.setdefault(
            node.name, len(self.func_replacements))
        new_name = f'func_{new_id:0>5}'
        result = ast.FunctionDef(name=new_name, args=node.args, body=node.body,
                                 decorator_list=node.decorator_list)
        return ast.copy_location(result, node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self._delete_docstring(node)
        self.generic_visit(node)

        new_id = self.class_replacements.setdefault(
            node.name, len(self.class_replacements))
        new_name = f'class_{new_id:0>5}'
        result = ast.ClassDef(
            name=new_name, bases=node.bases,
            keywords=node.keywords, body=node.body,
            decorator_list=node.decorator_list)

        return ast.copy_location(result, node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._delete_annotation(node)
        self._rename_args(node)
        self._delete_docstring(node)
        self.generic_visit(node)

        new_id = self.asyncfunc_replacements.setdefault(
            node.name, len(self.asyncfunc_replacements))
        new_name = f'func_{new_id:0>5}'
        result = ast.AsyncFunctionDef(
            name=new_name, args=node.args,
            body=node.body, decorator_list=node.decorator_list)

        return ast.copy_location(result, node)

    def visit_Module(self, node: ast.Module):
        self._delete_docstring(node)
        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name):
        new_id = self.name_replacements.setdefault(
            node.id, len(self.name_replacements))
        new_name = f'var_{new_id:0>5}'
        result = ast.Name(id=new_name)
        return ast.copy_location(result, node)

    def _is_docstring(self, node: ast.AST):
        is_docstring = True
        is_docstring = is_docstring and len(node.body)
        is_docstring = is_docstring and isinstance(node.body[0], ast.Expr)
        is_docstring = is_docstring and hasattr(node.body[0], 'value')
        is_docstring = is_docstring and isinstance(node.body[0].value,
                                                   ast.Constant)
        return is_docstring

    def _delete_docstring(self, node: ast.AST):
        if self._is_docstring(node):
            del node.body[0]

    def _delete_annotation(self, node: ast.AST):
        for arg in node.args.args:
            del arg.annotation
        del node.returns

    def _rename_args(self, node: ast.AST):
        for i, arg in enumerate(node.args.args):
            arg.arg = f'arg_{i}'


def main():
    tree = ast.parse("def f():\tprint('hello')\nf()")
    print(ast.dump(tree))


if __name__ == '__main__':
    main()
