class Pencil:

    def __init__(self, pencil_length, pencil_durability, eraser_durability):
        self.pencil_length = pencil_length
        self.remaining_length = pencil_length
        self.pencil_durability = pencil_durability
        self.remaining_durability = pencil_durability
        self.eraser_durability = eraser_durability
    
    def _text_capacity(text):
        """
        Method to calculate the durability points required to write a given text.
        The upper case letter takes extra durability point
        """
        capacity = len(text)
        for character in text:
            if character.isUpper():
                capacity += 1
        return capacity
    
    def write(self, sheet, text):
        """
        Method to write a given text to a sheet.
        The writing reduces the durability of the pencil.
        """
        text_capacity = self._text_capacity(text)
        if text_capacity <= self.remaining_durability:
            self.remaining_durability = self.remaining_durability - text_capacity
            result = text
        else:
            result = ""
            for character in text:
                if character == " ":
                    result += character
                elif character.isUpper():
                    if self.remaining_durability >= 2:
                        self.remaining_durability -= 2
                        result += character
                    else:
                        result += " "
                else:
                    if self.remaining_durability > 0:
                        self.remaining_durability -= 1
                        result += character
                    else:
                        result += " "
        sheet += result
        return sheet

    def sharpen(self):
        if self.remaining_length > 0:
            self.remaining_length = self.remaining_length - 1
            self.remaining_durability = self.pencil_durability
        return self.remaining_length

    def erase(self, text, word):
        if self.eraser_durability >= len(word.replace(" ", "")):
            self.eraser_durability -= len(word.replace(" ", ""))
            replace_word = " " * len(word)
        else:
            replace_word = ""
            for character in word[::-1]:
                if self.eraser_durability > 0:
                    self.eraser_durability -= 1
                    replace_word += " "
                else:
                    replace_word += character
        text = text.rsplit(word, 1)
        return replace_word.join(text)

    def edit(self, sheet, word):
        """
        Assuming during the edit, if there is a character collision, the replacing character with '@' is done in two steps
            1. Erase the existing character (Reduces eraser durability)
            2. Write the '@' character (Reduces pencil durability by 1 (same as lower case letter))
        """
        sheet_list = list(sheet)
        split_words = sheet.split("  ")
        # Idenitify the index of the first blank space by assuming more than 1 space as a blank.
        # This can be up to discussion whether we can treat more than 2 consecutive spaces as a blank
        # Or more than 3 consecutive spaces as a blank
        start_index = len(split_words[0]) + 1
        index = start_index
        for character, replace_character in zip(sheet[start_index:], word):
            if self.remaining_durability > 1:
                if character == " ":
                    sheet_list[index] = replace_character
                    self.remaining_durability -= 1
                else:
                    if self.eraser_durability >= 1:
                        self.eraser_durability -= 1
                        sheet_list[index] = "@"
                        # Assuming the durability point for '@' is same as lower case letter
                        self.remaining_durability -= 1
                    else:
                        # Assuming we replace the character collision only if we can erase
                        # So ignoring if the character cannot be erased
                        # The "else" part of the code is not needed, just adding it for understanding
                        pass
            elif self.eraser_durability > 1:
                sheet_list[index] = " "
                self.eraser_durability -= 1
            else:
                break
            index += 1

        return "".join(sheet_list)


pencil = Pencil(
    pencil_length=10,
    pencil_durability=40000,
    eraser_durability=1000
)

sheet = "She sells sea shells"
pencil.write(sheet, " down by the sea shore")

pencil.sharpen()

sheet = "How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
pencil.erase(sheet, "chuck")

sheet = "An       a day keeps the doctor away"
print(pencil.edit(sheet, "artichoke"))
