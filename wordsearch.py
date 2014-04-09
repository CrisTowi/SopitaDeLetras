#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import ascii_uppercase
from random import choice

W2E, E2W, N2S, S2N, NW2SE, NE2SW, SW2NE, SE2NW = range(8)
# Las direcciones a las que podemos ir

def word_search_base(width, height):
    """Genera un arreglo de caracteres aleatorios"""
    
    columns = []
    # 2D list
    for i in range(width):
        columns.append([choice(ascii_uppercase) for j in range(height)])
    return columns

def insert(word, puzzle, x, y, direction=W2E, inplace=True):
    """Insert a word into a puzzle starting at (x, y) going in the
    specified direction.
    
    Returns a list of newly occupied coordinates and the modified
    puzzle.
    
    """
    
    coords = []
    if not inplace:
        new_puzzle = [[j for j in i] for i in puzzle]
    else:
        new_puzzle = puzzle
    if direction == W2E:
        # going right
        i = x
        for char in word:
            if i < 0:
                raise IndexError
            # Prevent weird word wrapping behavior w/ negative indices
            new_puzzle[i][y] = char
            coords.append((i, y))
            i += 1
    elif direction == E2W:
        # going left
        i = x
        for char in word:
            if i < 0:
                raise IndexError
            new_puzzle[i][y] = char
            coords.append((i, y))
            i -= 1
    elif direction == N2S:
        # going down
        i = y
        for char in word:
            if i < 0:
                raise IndexError
            new_puzzle[x][i] = char
            coords.append((x, i))
            i += 1
    elif direction == S2N:
        # going up
        i = y
        for char in word:
            if i < 0:
                raise IndexError
            new_puzzle[x][i] = char
            coords.append((x, i))
            i -= 1
    elif direction == NW2SE:
        # going down and right
        i, j = x, y
        for char in word:
            if i < 0 or j < 0:
                raise IndexError
            new_puzzle[i][j] = char
            coords.append((i, j))
            i += 1
            j += 1
    elif direction == NE2SW:
        # going down and left
        i, j = x, y
        for char in word:
            if i < 0 or j < 0:
                raise IndexError
            new_puzzle[i][j] = char
            coords.append((i, j))
            i -= 1
            j += 1
    elif direction == SW2NE:
        # going up and right
        i, j = x, y
        for char in word:
            if i < 0 or j < 0:
                raise IndexError
            new_puzzle[i][j] = char
            coords.append((i, j))
            i += 1
            j -= 1
    elif direction == SE2NW:
        # going up and left
        i, j = x, y
        for char in word:
            if i < 0 or j < 0:
                raise IndexError
            new_puzzle[i][j] = char
            coords.append((i, j))
            i -= 1
            j -= 1
    return coords, new_puzzle

def word_search(width, height, words):
    """Create a word search with the specified words."""
    
    assert width * height > len("".join(words)), \
           "Too many words for a %sx%s puzzle" % (width, height)
    max_length = 0
    for word in words:
        if len(word) > max_length:
            max_length = len(word)
    assert max_length <= width or max_length <= height, \
           "At least one word is too long for a %sx%s puzzle" % (width, height)
    # Make sure there's enough room
    base = word_search_base(width, height)
    occupied = []
    # occupied coordinates
    word_coords = {}
    # {word: (x, y)}
    for word in words:
        word = word.upper()
        while 1:
            direction = choice(range(8))
            x, y = choice(range(width)), choice(range(height))
            # random direction + coords
            try:
                coords, new_puzzle = insert(word, base, x, y,
                                            direction=direction,
                                            inplace=False)
            except IndexError:
                # Word extends beyond the edge of the puzzle
                continue
            else:
                need_retry = False
                if [c for c in coords if c in occupied]:
                    for i, j in coords:
                        if (i, j) in occupied and \
                           base[i][j] != new_puzzle[i][j]:
                            # space conflict
                            need_retry = True
                            break
                if not need_retry:
                    insert(word, base, x, y, direction=direction)
                    occupied += coords
                    word_coords[word] = coords[0]
                    break
    return base, word_coords

def print_puzzle(puzzle, height, width):

    for k in range(width):
        print str(k)+'\t',
    print k+1,
    print
    for i in range(height):
        print str(i+1),
        for j in range(width):
            print str('\t'+puzzle[j][i]),
        print

if __name__ == "__main__":
    from random import sample
    from time import time
    
    print "Sopa de Letras! =D"
    width = 15
    height = 15
    print "Cargando palabras del archivo..."
    word_bank = open("enable1.txt").read().splitlines()
    word_bank = [w.lower() for w in word_bank if len(w) < width or
                 len(w) < height]
    # Filter out uneligible words (i.e. that are too long)
    word_bank = sample(word_bank, 10)
    print " Banco de palabras ".center(width * 2, "=")
    i = 0
    for word in word_bank:
        print word.center(width * 2)
    print "=" * width * 2
    # Show the word bank
    puzzle, word_coords = word_search(width, height, word_bank)

    print_puzzle(puzzle, height, width)

    start_time = time()
    print start_time
    # Start the timer
    words_found = []
    while len(words_found) < len(word_bank):
        word = raw_input("Qué palabra encontraste? ").lower()
        if word not in word_bank:
            # not in the word bank
            print 'No está en el banco de palabras ' + word
            continue
        coords = raw_input("Ingresa las coordenadas (separadas por comas) de 'x' 'y' de la palabra ")
        coords = coords.strip().strip("()").strip()
        # Remove parentheses and whitespace
        try:
            x, y = coords.split(",")
            x, y = int(x.strip()) - 1, int(y.strip()) - 1
        except ValueError, IndexError:
            # invalid format
            print "Las coordenadas deben estár separadas por comas"
            continue
        else:
            if (x, y) == word_coords[word.upper()]:
                words_found.append(word)
                print '"%s" encontrado!. %s faltantes.' % (
                    word, len(word_bank) - len(words_found)
                )
            else:
                # incorrect coordinates
                print 'La palabra ' + 'sí está en el bancon de letras pero no en las coordenadas especificadas'
    print "Felicidades! Completaste la sopa de letras en %d segundos." % (
        time() - start_time)
    # Show the time elapsed
 
