Talk at GCC 2017
================

> Building an open, collaborative, online infrastructure for bioinformatics training

# Abstract

With the advent of high-throughput platforms, life science data analysis is tightly linked to the use of bioinformatics tools, resources, and high-performance computing. However, the scientists who generate the data often do not have the knowledge required to be fully conversant with such analyses. To involve them in their own data analysis, these scientists must acquire bioinformatics vocabulary and skills through training.

Data analysis training is particularly challenging without a computational background. The Galaxy framework is addressing this problem by offering a web-based, intuitive and accessible user interface to numerous bioinformatics tools.

Recently, the Galaxy Training Network (GTN) set up a new open, collaborative, online model for delivering high-quality bioinformatics training material: http://galaxyproject.github.io/training-material.

Each of the current 12 topics provides tutorials with hands-on, slides and interactive tours. Tours are a new way to go through an entire analysis, step by step inside Galaxy in an interactive and explorative way. All material is openly reviewed, and iteratively developed in one central repository by 40 contributors. Content is written in Markdown and, similarly to Software/Data Carpentry, the model separates presentation from content. In addition, the technological infrastructure needed to teach each topic is described with a list of needed tools. The data (citable via DOI) required for the hands-on, time and resource estimations and flavored Galaxy Docker images are also provided.

This material is automatically propagated to Elixir's TeSS portal. With this community effort, the GTN offers an open, collaborative, FAIR and up-to-date infrastructure for delivering high-quality bioinformatics training for scientists.

# Usage

## Requirements

- [conda]()
- Create the conda environment:

    ```
    $ conda create -f environment.yml -n gcc_06_17
    ```

## Slide generation

The slides are written in markdown ([slides.md](slides.md)) and rendered using [reveal.js](https://github.com/hakimel/reveal.js/).

To visualize the slides, you need to launch a local server:

```
$ php -S localhost:8000
```

and then open any web browser at the adress: [http://localhost:8000](http://localhost:8000).

## GitHub statistics

- Launch the conda environment

    ```
    $ source activate gcc_06_17
    ```

- Generate a Personal access tokens on GitHub (in Setting)
    
- Extract statistics and contributors picture from the GitHub repository

    ```
    $ snakemake --snakefile src/extract_github_info.py
    ```

- Extract statistics about the GTN events on the Galaxy Hub

    ```
    $ snakemake --snakefile src/extract_hub_info.py
    ```

