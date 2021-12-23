import sys
import lookup_table
import parser
from tokenObject import TokenObj

# Global Variables

MAX_TOKEN_LENGTH = 100
MAX_LEXEME_LENGTH = 100
MAX_LINE_LENGTH = 50
open_index = 100
pos = 0
rpos = 0
lineNum = 0

currChar = None
nextChar = None
token = None
infile = None
outfile = None

lexeme = ''
line = ''
filename = ''
output_filename = ''

char_list = [''] * MAX_LEXEME_LENGTH
lex_list = []
token_list = []
output = [''] * 4


commentFlag = False
EOF_flag = False


def init():
    """
    Attempts to open the input and output files and prints an error message if the files cannot be opened.
    """
    global infile, outfile, lineNum, pos, filename, output_filename
    try:
        if len(sys.argv) >= 2:
            filename = sys.argv[1]
        else:
            filename = "hello_world.vbp"
            output_filename = filename.split('.')[0] + '.o'
        infile = open(filename)
    except OSError:
        print('error reading file')
    try:
        outfile = open(output_filename, 'w')
        outfile.write("### This Scanner expects source file written in Visual Basic ###\n")
        outfile.write("### Begin Printing Detected Tokens in " + filename + " ###\n")
        outfile.write("### Whitespace and comments are ignored ###\n\n")
    except OSError:
        print('error clearing output file')
    lineNum = -1
    pos = -1
    outfile.close()


def read():
    """
    Reads the next available line from the input file, then splits it into lexemes that can be tokenized
    ## Internal Recursive Functions ##
    add_letter(char)
    add_digit(char)
    add_strlit(char)
    add_sym(char)
    :return: None
    """
    global line, lex_list, lineNum, EOF_flag, char_list, rpos, commentFlag
    line = infile.readline()
    lineNum += 1
    char_list = []
    lex_list = []
    commentFlag = False

    if line == '':
        EOF_flag = True
    else:
        for c in line:
            char_list.append(c)

        spec_chars = "!@#$%^&*()[]{}<>?._\\|/,=-+`~"

        def add_letter(ch):
            """
            Recursively generates a string of letters and numbers from the character list
            :param ch: The character being added to the string
            :return: The completed string
            """
            global rpos
            str = ch
            rpos += 1
            if rpos < len(char_list)-1 and (char_list[rpos].isalnum() or char_list[rpos] == '_'):
                str += add_letter(char_list[rpos])
            return str

        def add_digit(ch):
            """
            Recursively generates a string of numbers from the character list
            :param ch: the number being added to the string
            :return: the completed string of numbers
            """
            global rpos
            str = ch
            rpos += 1
            if rpos < len(char_list)-1 and (char_list[rpos].isdigit() or char_list[rpos] == '.'):
                str += add_digit(char_list[rpos])
            return str

        def add_strlit(ch):
            """
            Recursively generates a string of characters from the character list if they are between two quotes
            :param ch: The character being added to the string
            :return: the completed string literal
            """
            global rpos
            str = ch
            rpos += 1
            if rpos < len(char_list)-1 and char_list[rpos] != '"':
                str += add_strlit(char_list[rpos])
            else:
                str += char_list[rpos]
                rpos += 1
            return str

        def add_sym(ch):
            """
            Recursively generates a string of special symbols from the character list if they are contained in the symbol
            list
            :param ch: the symbol being added to the string
            :return: the completed string of symbols
            """
            global rpos
            # spec_chars = "!@#$%^&*()[]{}<>?._\\|/,=-+`~"
            str = ch
            rpos += 1
            if rpos < len(char_list)-1 and any(c in spec_chars for c in char_list[rpos]):
                str += add_sym(char_list[rpos])
            return str

        rpos = 0
        while rpos < len(char_list):
            if char_list[rpos] == ' ' or char_list[rpos] == '\t' or char_list[rpos] == '':
                rpos += 1
            if char_list[rpos] == '\n':
                lex_list.append(char_list[rpos])
            if char_list[rpos].isalpha() or char_list[rpos] == '_':
                lex_list.append(add_letter(char_list[rpos]))
            elif char_list[rpos].isdigit():
                lex_list.append(add_digit(char_list[rpos]))
            elif char_list[rpos] == '"':
                lex_list.append(add_strlit(char_list[rpos]))
            elif any(c in spec_chars for c in char_list[rpos]):
                lex_list.append(add_sym(char_list[rpos]))
            else:
                rpos += 1


def tokenlookup(string):
    """
    Checks lookup_table.py for the token associated with the given string
    :param string: The string whose token you want to retrieve
    :return: an integer type token
    """
    global lex_list
    localtoken = 99

    if string[0].isalpha() or string[0] == '_':  # identifier or keyword
        if string in lookup_table.keyword_set:
            localtoken = lookup_table.KEYWORD
        else:
            localtoken = lookup_table.IDENTIFIER
    elif string[0].isdigit():
        localtoken = lookup_table.NUMERAL
    elif string[0] == '"':
        localtoken = lookup_table.STRING_LITERAL
    elif string[0] == '\'':
        localtoken = lookup_table.COMMENT
    elif string in lookup_table.terminator_set:
        localtoken = lookup_table.LINE_TERMINATOR
    elif string in lookup_table.type_char_set:
        localtoken = lookup_table.TYPE_CHARACTER
    elif string in lookup_table.operator_set:
        localtoken = lookup_table.OPERATOR
    elif string in lookup_table.separator_set:
        localtoken = lookup_table.SEPARATOR

    return localtoken


def lex():
    """
    Iterates through the constructed list of lexemes, determines the token associated with each and
    constructs the output string
    output string: "Token: <token>, Value: <lexeme>, At Line <lineNumber>, Character <characterNumber>
    :return: none
    """
    global lex_list, output, token, pos, commentFlag, open_index
    pos = 0
    str_val = ''
    if not EOF_flag:
        for s in lex_list:
            if s != '\n':
                token = tokenlookup(s)
                # if token is lookup_table.IDENTIFIER:
                #     if s not in lookup_table.identifier_set.values():
                #         lookup_table.identifier_set[open_index] = s
                #         open_index += 1
                if token is lookup_table.COMMENT:
                    commentFlag = True
                if not commentFlag:
                    setoutput('token', 'Token: ' + lookup_table.tokenToText[token] + '\t')
                    setoutput('lexeme', 'Value: \"' + s + '\"\t')
                    token_list.append(TokenObj(s, token))
                    setoutput('line_pos', 'At Line ' + str(lineNum) + ', ')
                    setoutput('char_pos', 'Character ' + str(pos))
                    writetofile(output)
                    pos += len(s) + 1
            else:
                token_list.append(TokenObj('\n', lookup_table.LINE_TERMINATOR))


def setoutput(t, value):
    """
    Updates the output list with a value at the position given by t
    :param t: expects a string associated with an index in the output list
    :param value: the string to be stored in the output list
    :return: None
    """
    global output
    output_dict = {
        'token': 0,
        'lexeme': 1,
        'line_pos': 2,
        'char_pos': 3
    }
    output[output_dict[t]] = value


def writetofile(string):
    """
    Writes the contents of string to the output file, followed by a newline symbol
    :param string: a list of strings to be output
    :return: None
    """
    global outfile
    try:
        outfile = open(output_filename, 'a')
    except OSError:
        print("ERROR - failed to open output file," + output_filename + '.o')
        quit()
    for e in string:
        outfile.write(e)
    outfile.write('\n')


# MAIN FUNCTION
def scan():
    """
    Main function. Calls init() to set up the files, and calls read() and lex() until an end of file flag is reached

    :return: None
    """
    global infile, EOF_flag
    print("Start Scanning.")
    init()
    while not EOF_flag:
        read()
        lex()

    ident_string = ''
    for key in lookup_table.identifier_set:
        ident_string += '\"' + lookup_table.identifier_set[key] + '\"' + '\t'
    writetofile("\n### List of detected Identifiers ###")
    writetofile(ident_string)
    infile.close()
    outfile.close()

    print("Output written to " + output_filename)
    print("Scanning Complete.")
    parser.parse(token_list)


scan()
