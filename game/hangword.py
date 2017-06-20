from sets import Set

class Hangword:
    def __init__(self, word):
        self._word = word
        self._wrong_guess = Set()
        self._progress_word = ['_'] * len(self._word)
        self.solved = False
    
    def operate(self, letter):
        if len(letter) > 1:
            raise Exception("input must be a single character, %s was entered instead" % (letter,))

        if letter in self._word:
            indexes = self._check_letter_positions(self._word, letter)
            for i in indexes:
                self._progress_word[i] = letter
        elif letter != '*':
            self._wrong_guess.add(letter)

        if self._check_if_completed():
            self.solved = True

    def _check_if_completed(self):
        return '_' not in self._progress_word
            
    def get_progress(self):
        return ' '.join(self._progress_word)

    def _check_letter_positions(self, word, letter):
        index_occurrences = []

        for i in range(0, len(word)):
            if word[i] == letter:
                index_occurrences.append(i)

        return index_occurrences

    def get_wrong_guesses(self):
        return list(self._wrong_guess)

    

    
            

    