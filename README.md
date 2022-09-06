<p align="center">
  <img src="assets/homescreen.gif" alt="Demo image"></img>
  <br/>
  <a href="#"><img src="https://img.shields.io/badge/c++-%2300599C.svg?style=flat&logo=c%2B%2B&logoColor=white"></img></a>
  <a href="http://opensource.org/licenses/MIT"><img src="https://img.shields.io/github/license/arthursonzogni/FTXUI?color=black"></img></a>
  <a href="#"><img src="https://img.shields.io/github/stars/ArthurSonzogni/FTXUI"></img></a>
  <a href="#"><img src="https://img.shields.io/github/forks/ArthurSonzogni/FTXUI"></img></a>
  <a href="#"><img src="https://img.shields.io/github/repo-size/ArthurSonzogni/FTXUI"></img></a>
  <a href="https://github.com/ArthurSonzogni/FTXUI/issues"><img src="https://img.shields.io/github/issues/ArthurSonzogni/FTXUI"></img></a>
  <a href="https://github.com/ArthurSonzogni/FTXUI/graphs/contributors"><img src="https://img.shields.io/github/contributors/arthursonzogni/FTXUI?color=blue"></img></a>
  <a href="https://codecov.io/gh/ArthurSonzogni/FTXUI">
    <img src="https://codecov.io/gh/ArthurSonzogni/FTXUI/branch/master/graph/badge.svg?token=C41FdRpNVA"/>
  </a>

  
  <br/>
  <a href="https://arthursonzogni.github.io/FTXUI/">Documentation</a> ·
  <a href="https://github.com/ArthurSonzogni/FTXUI/issues">Report a Bug</a> ·
  <a href="https://arthursonzogni.github.io/FTXUI/examples.html">Examples</a> .
  <a href="https://github.com/ArthurSonzogni/FTXUI/issues">Request Feature</a> ·
  <a href="https://github.com/ArthurSonzogni/FTXUI/pulls">Send a Pull Request</a>

</p>


<h1 align="center">Curses Based Cellular Automata</h1>

<p align="center">Life simulation using ASCII characters in Linux Terminal or Windows Command Prompt.</p>

## Links

- [Repo](https://github.com/Zadeson/Curses-Based-Cellular-Automata "Repo Page")

- [Bugs](https://github.com/Zadeson/Curses-Based-Cellular-Automata/issues "Issues Page")

## About

At program startup, the app prompts the user to enter every character they want included in the 'gene pool'.

### `Please enter every character you would like in the gene pool.`

The app automatically parses the input to remove spaces and duplicate characters. 
Every character included in this input will automatically be shown in the table, as well as reactive cells on the grid. Once the program is terminated (via pressing 'q') a graph will display, showing the population of each gene/character with an appropriate legend.

### `would you like to seperate each family? y/n`

At the start of the program, every gene/character is randomly created in a set area, depending on the input of this prompt. If the user answers 'y', every gene will be evenly distributed along the x axis of the screen, with the same y value. If the user answers with 'n', every gene will be randomly created in a small box at the center of the screen. 

### `Fight to the Death`

Watch as your chosen characters battle each other until only one family survives!

## Built With

- Python
  - windows-curses
  - time, random, os
  - matplotlib
  - numpy

## Todo

- [ ] More interactivity, possibly including a game-like function involving gambling.
- [ ] Making the app more visually appealing
- [ ] Adding settings for the user to tweak to their preferences
- [ ] DNA for individual cells?

## Screenshots

![Prompt](assets/prompt.png "Prompts for characters included in gene pool, and gene seperation.")

![A Running Simulation](assets/cellscr.png "A Running Simulation")

## Author

**Ethen Dixon**

- [Profile](https://github.com/Zadeson "Zadeson")
- [Email](mailto:ethendixon@outlook.com?subject=Hi "Hi!")

## 🤝 Support

Contributions, issues, and feature requests are welcome!

Give a ⭐️ if you like this project!
