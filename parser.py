import abstractMachine
import lookup_table
from abstractMachine import evaluate
from abstractMachine import P
from tokenObject import TokenObj


token_line = []
t_index = 0
identifier_index = 500
curr_token = TokenObj()
next_token = None
EOF = False


class ParseNode:
    def __init__(self, name='', prnt=None, chldrn=None):
        self._name = name
        self._parent = prnt
        self._children = chldrn

    def get_children(self):
        return self._children

    def add_child(self, node):
        if self._children is None:
            self._children = []
        if node is not None:
            self._children.append(node)

    def get_parent(self):
        return self._parent

    def get_name(self):
        return self._name

    def __str__(self, level=0):
        ret = '\t' * level + '|' + self._name + (':' if self.get_children() is not None else '') + '\n'
        if self._children is not None:
            for child in self._children:
                ret += child.__str__(level+1)
        return ret


currNode = ParseNode('root')


# Helper Functions
def nextToken():
    """
    Updates the curr_token variable to point to the next token in the token list
    :return: None
    """
    global t_index, curr_token, EOF, next_token
    t_index += 1
    if t_index < len(token_line):
        curr_token = token_line[t_index]
        if t_index + 1 < len(token_line):
            next_token = token_line[t_index + 1]
        else:
            next_token = curr_token
    else:
        EOF = True


# Parsing Rules
def start():
    """
    :return: returns a ParseNode object that represents the entire parse tree
    """
    print("Start Parsing.")
    thisNode = ParseNode('Start')
    while EOF is False:
        if curr_token.get_token() is not lookup_table.LINE_TERMINATOR:
            thisNode.add_child(namespaceMember(thisNode))
        nextToken()
    # print("End Parsing")
    return thisNode


def namespaceMember(parent):
    """
    Namespace Member Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: The ParseNode that called this rule
    :return: a ParseNode object representing a tree under thisNode
    """
    # print("Enter Namespace Member Declaration")
    thisNode = ParseNode('Namespace_Member_Declaration', parent)
    if curr_token.get_token() is not lookup_table.LINE_TERMINATOR:
        thisNode.add_child(namespaceDeclaration(thisNode))
        thisNode.add_child(moduleDeclaration(thisNode))
    if len(thisNode.get_children()) < 1:
        print("Syntax Error in Namespace Member Declaration. Expected \"Namespace\" or Type Declaration")
    # print("Exit Namespace Member Declaration")
    return thisNode


def namespaceDeclaration(parent):
    """
    Namespace Declaration rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: a ParseNode object representing the parent of thisNode in the tree
    :return: a ParseNode object representing the tree under thisNode
    """
    if curr_token.get_val() != 'Namespace' or curr_token.get_token() is lookup_table.LINE_TERMINATOR:
        return None
    # print("Enter Namespace Declaration")
    thisNode = ParseNode('Namespace_Declaration', parent)
    thisNode.add_child(ParseNode('\'' + str(curr_token.get_val() + '\''), parent))
    nextToken()
    thisNode.add_child(identifier(thisNode))
    nextToken()
    while curr_token.get_val() != "End":
        thisNode.add_child(namespaceMember(thisNode))
        nextToken()
    thisNode.add_child(ParseNode('\'' + str(curr_token.get_val() + '\''), parent))
    nextToken()  # we had to hit End by this point
    if curr_token.get_val() != "Namespace":
        print("Syntax Error. Expected \"Namespace\". Found \"" + str(curr_token.get_val()))
        return None
    # print("Exit Namespace Statement")
    return thisNode


def typeDeclaration(parent):
    """
    Type Declaration
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: a ParseNode object representing the node that called this rule
    :return: a ParseNode object representing the tree under thisNode
    """
    # print("Enter Type Declaration")
    thisNode = ParseNode('Type_Declaration', parent)
    thisNode.add_child(moduleDeclaration(thisNode))
    if len(thisNode.get_children()) < 1:
        print("Error in Type Declaration")
        return None
    # print("Exit Type Declaration")
    return thisNode


def moduleDeclaration(parent):
    """
    Module Declaration Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: a ParseNode object representing the node calling this rule
    :return: a ParseNode object representing the tree under thisNode
    """
    error = 'Syntax error in Module Declaration. '
    if curr_token.get_val() != 'Module':
        print(error + 'Expected \"Module\". Found ' + str(curr_token.get_val()))
        return None
    # print("Enter Module Declaration")
    thisNode = ParseNode('Module_Declaration', parent)
    thisNode.add_child(ParseNode('\'' + str(curr_token.get_val() + '\''), parent))
    nextToken()
    thisNode.add_child(identifier(thisNode))
    if thisNode.get_children() is None:
        print(error + 'Expected Identifier. Found ' + str(curr_token.get_val()))
        return None
    nextToken()
    while curr_token.get_val() != 'End' and not EOF:
        if curr_token.get_token() is lookup_table.LINE_TERMINATOR:
            nextToken()
        thisNode.add_child(moduleMemberDeclaration(thisNode))

    if EOF:
        print(error + 'End Symbol not reached')
        return thisNode
    else:  # has hit the end symbol
        thisNode.add_child(ParseNode('\'' + str(curr_token.get_val() + '\''), parent))
        nextToken()
        if curr_token.get_val() != 'Module':
            print(error + 'Expected \"Module\". Found ' + str(curr_token.get_val()))
            return thisNode
        thisNode.add_child(ParseNode('\'' + str(curr_token.get_val() + '\''), parent))
    # print("Exit Module Declaration")
    return thisNode


def objectCreationExpression(parent):
    """
    Object Creation Expression Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: a ParseNode object. Represents the node that called this rule
    :return: a ParseNode object. Represents the tree under thisNode
    """
    # print('Enter Object Creation Expression')
    thisNode = ParseNode('Object Creation Expression')
    if curr_token.get_val() != 'New':
        print('Syntax Error in Object Creation Expression')
        return None
    nextToken()
    thisNode.add_child(typeName(thisNode))
    nextToken()
    if curr_token.get_val() == '(':
        nextToken()
        thisNode.add_child(argumentList(thisNode))
    nextToken()
    if curr_token.get_val() != ')':
        print('Invalid Argument List')
        return None
    nextToken()
    # print('Exit Object Creation Expression')
    return thisNode


def typeName(parent):
    """
    Type Name Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print('Enter Type Name')
    thisNode = ParseNode('Type_Name', parent)
    if curr_token.get_val() not in lookup_table.primitive_set:
        print("Error. Invalid Type")
        return None
    thisNode.add_child(ParseNode("\"" + str(curr_token.get_val()) + "\""))
    # print('Exit Type Name')
    return thisNode


def variableMemberDeclaration(parent):
    """
    Variable Member Declaration Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    if curr_token.get_token() is not lookup_table.IDENTIFIER:
        return None
    # print('Enter Variable Member Declaration')
    thisNode = ParseNode('Variable_Member_Declaration')
    while curr_token.get_token() is lookup_table.IDENTIFIER:
        thisNode.add_child(identifier(thisNode))
        nextToken()
        if curr_token.get_val() == ',':
            nextToken()
    if curr_token.get_val() != 'As':
        print('Syntax Error in Variable Member Declarator')
        return thisNode
    nextToken() # next token is 'As'
    thisNode.add_child(objectCreationExpression(thisNode))
    # print('Exit Variable Member Declaration')
    return thisNode


def moduleMemberDeclaration(parent):
    """
    Module Member Declaration Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print('Enter Module Member Declaration')
    thisNode = ParseNode('Module_Member_Declaration')
    while curr_token.get_val() != 'End':
        thisNode.add_child(variableMemberDeclaration(thisNode))
        thisNode.add_child(subDeclaration(thisNode))
        nextToken()
        if curr_token.get_token() is lookup_table.LINE_TERMINATOR:
            nextToken()
    if thisNode.get_children() is None:
        print('Error in Module Member Declaration')
        return None
    # print('Exit Module Member Declaration')
    return thisNode


def subDeclaration(parent):
    """
    Subroutine Declaration Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print("Enter Sub Declaration")
    thisNode = ParseNode('Sub_Declaration', parent)
    error = 'Syntax Error in Sub Declaration. '
    thisNode.add_child(subSignature(thisNode))
    nextToken()
    if curr_token.get_token() is lookup_table.LINE_TERMINATOR:
        nextToken()
    thisNode.add_child(block(thisNode))
    if curr_token.get_val() != 'End':
        print(error + 'Expected End Symbol. Found \'' + str(curr_token.get_val()) + '\'')
    thisNode.add_child(ParseNode('\'' + str(curr_token.get_val() + '\''), parent))
    nextToken()
    if curr_token.get_val() != 'Sub':
        print(error + 'Expected \"Sub\". Found \'' + str(curr_token.get_val()) + '\'')
    thisNode.add_child(ParseNode('\'' + str(curr_token.get_val() + '\''), parent))
    # print("Exit Sub Declaration")
    return thisNode


def block(parent):
    """
    Block Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print("Enter Block")
    thisNode = ParseNode('Block', parent)
    while curr_token.get_val() != 'End':
        thisNode.add_child(statement(thisNode))
        nextToken()
        if curr_token.get_token() is lookup_table.LINE_TERMINATOR:
            nextToken()
    # print("Exit Block")
    return thisNode


def subSignature(parent):
    """
    Subroutine Signature Declaration Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print("Enter Sub Signature")
    thisNode = ParseNode("Sub_Signature", parent)
    error = 'Syntax Error in ' + thisNode.get_name() + ' '
    if curr_token.get_val() != "Sub":
        print(error + 'Expected \"Sub\". Found \"' + str(curr_token.get_val()) + '\'')
        return None
    nextToken()
    thisNode.add_child(identifier(thisNode))
    if thisNode.get_children() is None:
        print(error + 'Expected Identifier. Found ' + lookup_table.tokenToText(curr_token.get_token()))
        return None
    nextToken()
    if curr_token.get_val() not in {'(', '()'}:
        print(error + 'Expected Parameter List. Found \"' + str(curr_token.get_val()) + '\'')
        return None
    if curr_token.get_val() == '(':
        thisNode.add_child(parameterList(thisNode))
        nextToken()
        if curr_token.get_val() != ')':
            print(error + 'Invalid Parameter List')
            return None

    # print("Exit Sub Signature")
    return thisNode


def identifier(parent):
    global identifier_index
    """
    Identifier Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    thisNode = ParseNode('Identifier', parent)
    if curr_token.get_token() is not lookup_table.IDENTIFIER:
        return None
    thisNode.add_child(ParseNode('\'' + str(curr_token.get_val()) + '\'', parent))
    found = True
    if str(curr_token.get_val()) not in lookup_table.identifier_set.values():
        lookup_table.identifier_set[identifier_index] = curr_token.get_val()
        identifier_index += 1
        found = False
    P.append(curr_token.get_token())
    if found:
        for key, value in lookup_table.identifier_set.items():
            if value == curr_token.get_val():
                P.append(key)
    else:
        P.append(identifier_index - 1)
    # print('Identifier')
    return thisNode


def statement(parent):
    """
    Statement Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print("Enter Statement")
    thisNode = ParseNode('Statement', parent)
    error = 'Syntax Error in Statement'
   # thisNode.add_child(invocationStatement(thisNode))
   # if thisNode.get_children() is None:
    thisNode.add_child(localDeclarationStatement(thisNode))
    if len(thisNode.get_children()) == 0:
        thisNode.add_child(assignmentStatement(thisNode))
    # other statements here
    # print("Exit Statement")
    return thisNode


def additionStatement(parent):
    thisNode = ParseNode('Addition_Statement')
    thisNode.add_child(additionOperator(thisNode))
    nextToken()
    thisNode.add_child(expression(thisNode))
    P.append(lookup_table.OPERATOR)
    P.append('+')
    return thisNode


def additionOperator(parent):
    thisNode = ParseNode('Addition Operator')
    if curr_token.get_val() == "+":
        thisNode.add_child(ParseNode("\"" + str(curr_token.get_val() + "\"")))
        # P.append(curr_token.get_token())
        # P.append(curr_token.get_val())
        return thisNode
    else:
        return None


def localDeclarationStatement(parent):
    thisNode = ParseNode('Local_Declaration_Statement')
    thisNode.add_child(localModifier(thisNode))
    if len(thisNode.get_children()) == 0:
        return None
    nextToken()
    thisNode.add_child(identifier(thisNode))
    nextToken()
    if curr_token.get_val() != 'As':
        print("Syntax error in Local Declaration, missing \"As\"")
        return None
    thisNode.add_child(ParseNode('\"' + str(curr_token.get_val()) + '\"'))
    nextToken()
    thisNode.add_child(typeName(thisNode))
    return thisNode


def localModifier(parent):
    thisNode = ParseNode('Local_Modifier')
    if curr_token.get_val() not in {'Static', 'Dim', 'Const'}:
        return None
    thisNode.add_child(ParseNode("\"" + str(curr_token.get_val()) + "\"", thisNode))
    return thisNode


def assignmentStatement(parent):
    thisNode = ParseNode('Assignment_Statement', parent)
    thisNode.add_child(expression(thisNode))
    nextToken()
    thisNode.add_child(assignmentOperator(thisNode))
    if thisNode.get_children() is None:
        return None
    nextToken()
    thisNode.add_child(expression(thisNode))
    if thisNode.get_children() is None:
        return None
    P.append(lookup_table.OPERATOR)
    P.append('=')
    return thisNode


def assignmentOperator(parent):
    thisNode = ParseNode('Assignment_Operator', parent)
    if curr_token.get_val() != '=':
        return None
    thisNode.add_child(ParseNode('\"=\"', parent))
    # P.append(curr_token.get_token())
    # P.append(curr_token.get_val())
    return thisNode


def invocationStatement(parent):
    """
    Invocation Statement Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print('Enter Invocation Statement')
    thisNode = ParseNode('Invocation_Statement', parent)
    if curr_token.get_val() == 'Call':
        nextToken()
    thisNode.add_child(invocationExpression(thisNode))
    if thisNode.get_children() is None:
        print('Invalid Invocation Statement')
        return None
    # print('Exit Invocation Statement')
    return thisNode


def argumentList(parent):
    """
    Argument List Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print('Enter Argument List')
    thisNode = ParseNode('Argument_List', parent)
    while curr_token.get_val() != ')':
        if curr_token.get_val() == ',':
            nextToken()
        thisNode.add_child(identifier(thisNode))
        thisNode.add_child(literal(thisNode))
        nextToken()
    if thisNode.get_children() is None:
        print('Syntax Error from ' + thisNode.get_parent().get_name() + '. Invalid Argument List')
        return None
    # print('Exit Argument List')
    return thisNode


def literal(parent):
    """
    Literal Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    thisNode = ParseNode('Literal', parent)
    if curr_token.get_token() not in {lookup_table.STRING_LITERAL, lookup_table.NUMERAL}:
        return None
    thisNode.add_child(ParseNode('\'' + str(curr_token.get_val()) + '\'', thisNode))
    P.append(curr_token.get_token())
    P.append(curr_token.get_val())
    # print('Literal')
    return thisNode


def invocationExpression(parent):
    """
    Invocation Expression Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print('Enter Invocation Expression')
    thisNode = ParseNode('Invocation_Expression', parent)
    thisNode.add_child(expression(thisNode))
    if len(thisNode.get_children()) < 1 or curr_token.get_val() not in {'(', '()'}:
        print('Error in Invocation Expression')
        return None
    thisNode.add_child(ParseNode('\'' + str(curr_token.get_val()) + '\'', parent))
    nextToken()
    thisNode.add_child(argumentList(thisNode))
    if curr_token.get_val() != ')':
        print('Error in Invocation Expression')
        return None
    thisNode.add_child(ParseNode('\'' + str(curr_token.get_val()) + '\'', parent))
    # print('Exit Invocation Expression')
    return thisNode


def expression(parent):
    """
    Expression Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print('Enter Expression')
    thisNode = ParseNode('Expression', parent)
    done = False
    while not done:
        thisNode.add_child(literal(thisNode))
        thisNode.add_child(identifier(thisNode))
        if next_token.get_val() == '.':
            nextToken()
            thisNode.add_child(ParseNode('\'' + str(curr_token.get_val()) + '\'', parent))
        elif (next_token.get_token() is lookup_table.OPERATOR) and not (next_token.get_val() == '='):
            nextToken()
            switch = {
                '+': thisNode.add_child(additionStatement(thisNode)),
                '-': None,
                '*': None,
                '/': None
            }
            switch.get(curr_token.get_val(), None)
            done = True
            # nextToken()
        else:
            done = True

    if len(thisNode.get_children()) < 1:
        print('Syntax Error in Expression, expected literal or identifier')
        return None

    if curr_token.get_val() in {'(', '()'}:
        return thisNode
    # print('Exit Expression')
    return thisNode


def parameterList(parent):
    """
    Parameter List Rule
    Creates a ParseNode object, thisNode, representing a call to this rule
    :param parent: ParseNode object. Represents the node that called this rule
    :return: ParseNode object. Represents the tree under thisNode
    """
    # print("Enter Parameter List")
    thisNode = ParseNode('Parameter_List', parent)
    error = 'Syntax Error in Parameter List'
    if curr_token.get_token() is not lookup_table.IDENTIFIER:
        print(error + 'Expected Identifier. Found ' + lookup_table.tokenToText(curr_token.get_token()))
        return thisNode
    thisNode.add_child(identifier(thisNode))
    nextToken()
    if curr_token.get_val() == ',':
        thisNode.add_child(ParseNode(str(curr_token.get_val()), parent))
        nextToken()
        thisNode.add_child(parameterList(thisNode))
    # print("Exit Parameter List")
    return thisNode


def parse(token_list):
    """
    Main Function
    Creates a Parse Tree from a list of tokens using a subset off the BASIC grammar rules
    :param token_list: a list of detected tokens from the source file generated in scanner.py
    :return: None
    """
    global t_index, curr_token, token_line, next_token
    t_index = 0
    token_line = token_list
    curr_token = token_line[t_index]
    next_token = token_line[t_index + 1]
    topNode = start()
    print("Parsing Complete.")
    print('')
    print('Parse Tree:')
    print(topNode)
    print('Begin Abstract Machine')
    abstractMachine.evaluate()

