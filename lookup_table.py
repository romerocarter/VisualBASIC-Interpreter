# Tokens
IDENTIFIER = 10
KEYWORD = 11
STRING_LITERAL = 12
NUMERAL = 13
TYPE_CHARACTER = 14
COMMENT = 15
OPERATOR = 16
SEPARATOR = 17
UNKNOWN = 99
LINE_TERMINATOR = 18
LINE_CONTINUATION = 19

keyword_set = {
    'AddHandler', 'AddressOf', 'Alias', 'And', 'AndAlso', 'As', 'Boolean', 'ByRef', 'Byte', 'ByVal', 'Call', 'Case',
    'Catch', 'CBool', 'CByte', 'CChar', 'CDate', 'CDbl', 'CDec', 'Char', 'CInt', 'Class', 'CLng', 'CObj', 'Const',
    'Continue', 'CSByte', 'CShort', 'CSng', 'CStr', 'CType', 'CUInt', 'CULng', 'CUShort', 'Date', 'Decimal', 'Declare',
    'Default', 'Delegate', 'Dim', 'DirectCast', 'Do', 'Double', 'Each', 'Else', 'ElseIf', 'End', 'EndIf', 'Enum',
    'Erase', 'Error', 'Event', 'Exit', 'False', 'Finally', 'For', 'Friend', 'Function', 'Get', 'GetType',
    'GetXmlNamespace', 'Global', 'GoSub', 'GoTo', 'Handles', 'If', 'Implements', 'Imports', 'In', 'Inherits', 'Integer',
    'Interface', 'Is', 'IsNot', 'Let', 'Lib', 'Like', 'Long', 'Loop', 'Me', 'Mod', 'Module', 'MustInherit',
    'MustOverride', 'MyBase', 'MyClass', 'Namespace', 'Narrowing', 'New', 'Next', 'Not', 'Nothing', 'NotInheritable',
    'NotOverridable', 'Object', 'Of', 'On', 'Operator', 'Option', 'Optional', 'Or', 'OrElse', 'Overloads',
    'Overridable', 'Overrides', 'ParamArray', 'Partial', 'Private', 'Property', 'Protected', 'Public', 'RaiseEvent',
    'ReadOnly', 'ReDim', 'REM', 'RemoveHandler', 'Resume', 'Return', 'SByte', 'Select', 'Set', 'Shadows', 'Shared',
    'Short', 'Single', 'Static', 'Step', 'Stop', 'String', 'Structure', 'Sub', 'SyncLock', 'Then', 'Throw', 'To',
    'True', 'Try', 'TryCast', 'TypeOf', 'UInteger', 'ULong', 'UShort', 'Using', 'Variant', 'Wend', 'When', 'While',
    'Widening', 'With', 'WithEvents', 'WriteOnly', 'Xor'
}

identifier_set = {}

type_char_set = {'%', '&', '@', '!', '#', '$'}

operator_set = {'&', '*', '+', '-', '/', '\\', '^', '<', '=', '>', '<<', '>>', '<>',
                '<=', '>='}

primitive_set = {'Boolean', 'Date', 'Char', 'String', 'Decimal', 'Byte',  'Byte',  'UShort',  'Short',  'UInteger',
                 'Integer',  'ULong',  'Long', 'Single',  'Double'}

separator_set = {'(', '()', ')', '{', '}', '!', '#', ',', '.', ':', '?'}

terminator_set = {'\u000D', '\u2028', '\u2029', '\u000D\u000A'}

tokenToText = {
    IDENTIFIER: 'Identifier',
    KEYWORD: 'Keyword',
    STRING_LITERAL: 'String Literal',
    NUMERAL: 'Numeral',
    TYPE_CHARACTER: 'Type Character',
    COMMENT: 'Comment',
    UNKNOWN: 'Unrecognized Token',
    OPERATOR: 'Operator',
    SEPARATOR: 'Separator',
    LINE_CONTINUATION: 'Line Continuation',
    LINE_TERMINATOR: 'Line Terminator'
}
# Grammar Definitions


