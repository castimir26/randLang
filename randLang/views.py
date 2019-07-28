from django.shortcuts import render
from django.http import HttpResponse
from randLang.models import Dict_Words
from randLang.models import User_Created
from io import BytesIO
from reportlab.pdfgen import canvas
from randLang.services import create_alphabet
from randLang.services import create_syllables
from randLang.services import enum_dict
from randLang.services import assemble_word
from randLang.services import con_select_all
import time
import random

# Create your views here.


def show_letters(request):

    '''
    Input: POST request (or really any request)
    Process:
        1. Create a dictionary with a full alphabet and full syllable patterns
    Output: Django httpresponse

    Note: The create_alphabet and create_syllable methods are meant to be modifiable
    for different orthographies or depth of syllable patterns. This is the container
    method.
    '''
    context_dict = {"letters": create_alphabet(), "syl_piece": create_syllables()}
    return render(request, 'show_letters.html', context_dict)


def generate_pdf(request):

    '''
    Input: http request
    Process:
        1. Create the http header
        2. Load the http request into a buffer using BytesIO -- see django tutorial
        3. create the pdf object and then a textobject instance
        4. Capture all of the form data
        5. Create intermediary strings for the pdf
        6. Load the word dictionary from the database and parse it, pulling out the word and stripping all other database
        7. Iterate over the user created word dictionary and grab the words_list
        8. Draw on pdf
        9. Close out pdf cleanly, render file response
    '''
    # Create the HttpResponse object with the appropriate PDF headers.
    # Step 1

    response = HttpResponse(content_type='application/pdf')
    page_counter = 0
    counter = 0
    eng_words_list = []

    # Step 2

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    # Step 3

    p = canvas.Canvas(buffer)
    textobject = p.beginText()
    textobject.setTextOrigin(10, 800)

    # Step 4
    # start creating the title

    language = request.POST.getlist('language')

    # use language in the filename of the download

    language_pdf = 'attachment; filename="' + language[0] + '".pdf'
    response['Content-Disposition'] = language_pdf

    # The only thing we want is the first value of the language list, which
    # provides the generated language

    real_language = language[0]

    # Get the existing words

    try:
        words = User_Created.objects.filter(language=real_language)
    except User_Created.DoesNotExist:
        context_dict = {"warning": "Database table 'User_Created' does not exist, did you forget to initiate the database?", "language": real_language}
        return render(request, 'show_lang.html', context_dict)
    try:
        english_word = Dict_Words.objects.all()
    except english_word.DoesNotExist:
        existing_warning = "Database table 'Dict_Words' does not exist, did you forget to initiate the database?"
        context_dict = {"warning": existing_warning, "language": real_language}
        return render(request, 'show_lang.html', context_dict)

    # create strings for pdfs

    translation = " translates loosely to the English word '"
    language_greeting = "This is the dictionary file for "

    # concatenate language greeting and language name to create a title for the pdf

    language_greeting += real_language

    # Step 5

    textobject.textLine(language_greeting)
    textobject.moveCursor(0, 10)

    # Step 6

    eng_words_list = enum_dict(english_word)

    # Step 7
    # "counter" keeps track of the number of times iterated and is used for indexing
    # "page_counter" keeps track of how many lines are in the pdf

    for key, word in enumerate(words):
        word_inst = word.user_word
        real_word = eng_words_list[counter]
        counter += 1
        word_inst += translation
        word_inst += real_word
        word_inst += "'"
        textobject.textLine(word_inst)
        textobject.moveCursor(0, 10)

    # step 8
    # drawText and showPage are required to move the cursor to the next pdf page

        if page_counter > 30:
            p.drawText(textobject)
            p.showPage()
            textobject = p.beginText()
            page_counter = 0
            textobject.setTextOrigin(10, 800)
        else:
            page_counter += 1

    # Step 9
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    p.drawText(textobject)

    # Close the PDF object cleanly.

    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def show_lang(request):
    '''
    This actually shows the generated language.
    Input: POST request
    Process:
        1. Iterate over letters in request.
        2. Assign weights to letters in a tuples
        3. Pass tuples, separated by vowel/consonant, to syllable method
        4. Append syllables as they return to word.
        5. Append word to list of words
    Output: Full list of words, in Django httpresponse
    '''
    vowel_list = [(random.SystemRandom().randint(1, 5), 'a'), (random.SystemRandom().randint(1, 5), 'e'), (random.SystemRandom().randint(1, 5), 'i'), (random.SystemRandom().randint(1, 5), 'o'), (random.SystemRandom().randint(1, 5), 'u')]
    consonant_list = []
    syllable_list = []
    weight_list = []
    first_word_list = []
    word_list = []
    if request.method == "POST":
        weight_list = request.POST.getlist('weight')

        # implements a select all

        if request.POST.getlist('selectall'):
            consonant_list = con_select_all(vowel_list, consonant_list)
        else:
            first_word_list = request.POST.getlist('letters')
            for x in range(0, len(first_word_list)):
                letter = first_word_list[x]
                weight = int(weight_list[x])
                # note: not using y or j as vowels. End user will have to determine if vowels are long or short
                if letter not in vowel_list:
                    consonant_list.append((weight, letter))
                else:
                    vowel_list.append((weight, letter))

        # fixes empty vowel and empty consonant problem

        if not consonant_list or not vowel_list:
            context_dict = {"warning": "You must have at least one vowel and one consonant", "letters": create_alphabet(), "syl_piece": create_syllables()}
            return render(request, 'show_letters_warning.html', context_dict)

        if request.POST.getlist('selectallsyl'):
            syllables = create_syllables()
        else:
            syllables = request.POST.getlist('syllables')
        for syllable in syllables:
            syllable_list.append((random.SystemRandom().randint(0, 100), syllable))

        # Fix empty syllable problem

        if not syllable_list:
            context_dict = {"warning": "You must choose at least one syllable pattern", "letters": create_alphabet(), "syl_piece": create_syllables()}
            return render(request, 'show_letters_warning.html', context_dict)

        # Pull up all words to assign them to generated words

        list_word = []
        try:
            all_words = Dict_Words.objects.all()
            list_word = enum_dict(all_words)
        except Dict_Words.DoesNotExist:
            word_warning = "Words do not exist in database, please contact administrator"
            context_dict = {"warning": word_warning, "letters": create_alphabet(), "syl_piece": create_syllables()}
            return render(request, 'show_letters_warning.html', context_dict)
        language = assemble_word(random.SystemRandom().randint(1, 5), syllable_list, vowel_list, consonant_list).capitalize()
        for x in range(0, len(list_word)):
            word = assemble_word(random.SystemRandom().randint(1, 5), syllable_list, vowel_list, consonant_list).capitalize()

            # TODO optimize this

            try:
                User_Created.objects.get_or_create(user_word=word, definition=list_word[x], language=language)
            except User_Created.DoesNotExit:
                create_warning = "Words do not exist in database, please contact administrator"
                context_dict = {"warning": create_warning, "letters": create_alphabet(), "syl_piece": create_syllables()}
                return render(request, 'show_letters_warning.html', context_dict)
            word_list.append((word, list_word[x]))

    context_dict = {"words": word_list, "language": language}
    ts = time.time()
    print(ts)
    return render(request, 'show_lang.html', context_dict)
