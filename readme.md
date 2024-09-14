# September 10th 2024 US Presidential Debate Word Cloud

## Prerequisites

Run `pip install nltk wordcloud matplotlib`

## Sources

Transcript by [The American Presidency Project](https://www.presidency.ucsb.edu/documents/presidential-debate-philadelphia-pennsylvania)

Donkey and elephant masks created from the party logos with minor blurring for smoothness and filling in the stars. Current dimensions max out at 4000 but the mask images can be scaled if a different resolution is desired.

## Methods

Import known stop words for english language and add a few custom ignore words like the names of the candidates and the word 'president' etc. to prevent the word clouds from being uninformative.

Ignore moderator conent and strip out each candidate's content, then generate 100 hi-res word clouds with varying random states.

## Usage

Run `python debatecloud.py`

Change `num_clouds` to set the number of clouds to generate per candidate.

Adjust WordCloud settings like `colormap`, `background_color` and `max_words` to experiment with various possibilities.

## Notes

This repoisitory exists so anyone can verify the methods are sound and use it to create their own variants.

## Random State 0 Samples

![Harris](harris_wordcloud_0.png)

![Trump](trump_wordcloud_0.png)