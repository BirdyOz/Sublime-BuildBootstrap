# Sublime-BuildBootstrap

## Build Bootstrap interface elements for Sublime Text

This SublimeText plugin allows you to rapidly develop Bootstrap interface elements, including:

* Accordions
* Tabs - both vertical and horizontal
* Show/hide
* Various card layouts and colours - cards, decks, rainbow and columns


![Screencapture](tests/screencap.png)


### Note

* Each UI element is given a unique ID to avoid one element accidentally controlling another (eg. if you have two accordions on the one page)
* for card based interfaces, any more than three cards will automatically default to column view


## Video tutorial

[Build Bootstrap interface elements for Sublime Text (08:12)](https://www.youtube.com/embed/Z8MGYE1QJCc?rel=0)

## Dependancies

This plugin invokes functions from other Sublime Text Packages:

<ul>
    <li><a href="https://packagecontrol.io/packages/HTML-CSS-JS%20Prettify" target="_blank">HTML-CSS-JS Prettify - Packages - Package Control</a></li>
</ul>

Please ensure that you have this plugin installed, **prior to running BuildBootstrap**

## Usage

1. Launch Package Control
2. Type 'Build Bootstrap'
3. Choose Bootstrap interface element

## Keyboard shortcuts (Mac) - Sorry Windows users, feel free to set your own.

The use a chain of two commands, in quick succession, eg:



* ⌃⌥⌘**B**, ⌃⌥⌘**A**  - **B**uild Accordion
* ⌃⌥⌘**B**, ⌃⌥⌘**T**  - **B**uild **T**abs (Vertical)
* ⌃⌥⌘**B**, ⌃⌥⌘**H**  - **B**uild Tabs (**H**orizontal)
* ⌃⌥⌘**B**, ⌃⌥⌘**S**  - **B**uild **S**how/Hide
* ⌃⌥⌘**B**, ⌃⌥⌘**C**  - **B**uild **C**ards
* ⌃⌥⌘**B**, ⌃⌥⌘**D**  - **B**uild Card **D**eck
* ⌃⌥⌘**B**, ⌃⌥⌘**R**  - **B**uild **R**ainbow Cards