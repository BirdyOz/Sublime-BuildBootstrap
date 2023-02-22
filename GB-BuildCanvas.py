import sublime, sublime_plugin, string
from datetime import date, time
today = date.today()

# Define HTML code snippets
snippets = {
    "Accordion":
        {
        "Start": '\n<div class="uom-ui-accordion">',
        "Repeat": '\n<div class="uom-ui-accordion-trigger"> <span class="uom-ui-accordion-title">{a}</span> </div> <div class="uom-ui-accordion-panel">{b}</div>',
        "End": '</div>\n'
        },
    "V-tabs":
    {
        "Start": '\n<div class="uom-ui-tab uom-ui-vertical">',
        "Nav-Start": '<div class="uom-ui-tablist" aria-label="tabcontent">',
        "Nav-Repeat": '<div class="uom-ui-trigger">{a}</div>',
        "Nav-End": '</div>',
        "Repeat": '\n<div class="uom-ui-tab-panel"> <h3>{a}</h3>\n {b} </div> \n',
        "End": '</div> \n'
    },
    "H-tabs":
    {
        "Start": '\n<div class="uom-ui-tab">',
        "Nav-Start": '<div class="uom-ui-tablist" aria-label="tabcontent">',
        "Nav-Repeat": '<div class="uom-ui-trigger">{a}</div>',
        "Nav-End": '</div>',
        "Repeat": '\n<div class="uom-ui-tab-panel"> <h3>{a}</h3>\n {b} </div> \n',
        "End": '</div> \n'
    },
    "Tiles":
    {
        "Start": '\n<ul class="uom-ui-grid uom-with-border uom-ui-tiles-tight">',
        "Repeat": '\n<li> <div class="tile-body"> <h3>{a}</h3>\n {b}\n</div> </li> \n',
        "End": '</ul> \n'
    },
    "Deaf":
    {
        "Start": '\n<p class="uom-ui-reveal uom-ui-button" style="background-color: #8b547e; color: #fff;"><i class="fas fa-sign-language"></i> Specialist stream - Deaf Education (click to view)</p>\n<div class="uom-ui-hidden-content">\n <div class="uom-ui-border-box uom-ui-add-border-radius" style="border-color: #8b547e; clear: both;">\n <h2 style="color: #8b547e;"><i class="fas fa-sign-language"></i> Specialist stream - Deaf Education</h2>\n',
        "Repeat": '<h3>{a}</h3>{b}\n',
        "End": '</div>\n</div>\n'
    },
    "Neurodiversity":
    {
        "Start": '\n<p class="uom-ui-reveal uom-ui-button" style="background-color: #469999; color: #fff;"><i class="fas fa-cubes"></i> Specialist stream - Neurodiversity (click to view)</p>\n<div class="uom-ui-hidden-content">\n <div class="uom-ui-border-box uom-ui-add-border-radius" style="border-color: #469999; clear: both;">\n <h2 style="color: #469999;"><i class="fas fa-cubes"></i> Specialist stream - Neurodiversity</h2>\n',
        "Repeat": '<h3>{a}</h3>{b}\n',
        "End": '</div>\n</div>\n'
    },
    "Show":
    {
        "Start": '\n<!-- Start of Canvas Show interface, date = {t} -->',
        "Repeat": '<p class="uom-ui-reveal uom-ui-button uom-primary" data-afterclick="hideinplace">{a} (Show me more)</p><div class="uom-ui-hidden-content uom-ui-emphasise"><h3>{a}<h3>\n{b}</div>',
        "End": ' \n'
    },
    "Box-Template":
    {
        "Start": '',
        "Repeat": '\n<div class="uom-ui-border-box uom-ui-add-border-radius" style="border-color: {bc}; clear: both"> <h3 style=" color: {bc}"><i class="{bi} fa-fw"></i> {tp}{a}{ts}</h3> \n {b}\n{bf}</div> \n',
        "End": ''
    },
    "Box-Idea": {
                "Box-Colour": "#094183",
                "Box-Icon": 'far fa-lightbulb'
            },
    "Box-Reading": {
                "Box-Colour": "#094183",
                "Box-Icon": 'fab fa-leanpub'
            },
    "Box-Important": {
                "Box-Colour": "#094183",
                "Box-Icon": 'fas fa-exclamation-triangle'
            },
    "Box-Law": {
                "Box-Colour": "#094183",
                "Box-Icon": 'fas fa-balance-scale-left',
                "Box-Footer": '<div class="uom-ui-notice--info">Check with the library or your workplace for a copy of this law/standard</div>'
            },
    "Box-OSS": {
                "Box-Colour": "#094183",
                "Box-Icon": 'fas fa-cogs',
                "Title-Prefix": 'Optional Self Study'
            },
    "Box-DET": {
                "Box-Colour": "#094183",
                "Box-Icon": 'fas fa-cogs',
                "Title-Prefix": 'Department of Education and Training Victoria resource'
            },
    "Box-Discuss": {
                "Box-Repeat": " mt-1 mb-1",
                "Title-Prefix": "Discussion Activity",
                "Box-Colour": " text-danger",
                "Box-Icon": 'fa-tasks',
                "Box-Footer": '<div class="alert alert-success" role="alert"> Record your responses in the [exact name of discussion activity] forum that follows this content. </div>'
            },
    "Box-Reflect": {
                "Title-Prefix": "Reflection",
                "Box-Colour": " #22765f;",
                "Box-Icon": 'fas fa-head-side-virus',
                "Box-Footer": '<div class="uom-ui-notice--success">Record your thoughts in your <strong>Reflective journal</strong>. These reflections will help you to better understand the content and prepare for assessment.</div>'
            },
    "Box-Video": {
                "Title-Suffix": " (MM:SS)",
                "Box-Colour": " #22765f;",
                "Box-Icon": 'fab fa-youtube'
            },
    "Box-Activity": {
                "Box-Colour": " #22765f;",
                "Box-Icon": 'fas fa-tasks'
            }
}


class BuildCanvasCommand(sublime_plugin.TextCommand):
    def run(self, edit, type):
        view = self.view
        for region in view.sel():
            if not region.empty():
                s = view.substr(region) # string of selected region
                scope = view.scope_name(view.sel()[0].begin())
                t = canvas_parser(s,type) # send string to parser

                view.replace(edit, region, t) # Update page content
                self.view.run_command("htmlprettify")
                if 'text.html.markdown' in str(scope):
                    self.view.run_command("delete_empty_lines")
                # self.view.sel().clear()

class QuickClickCommand(sublime_plugin.TextCommand):
    def run(self, edit, items):
        self.view.show_popup_menu(
            [item["caption"] for item in items],
            lambda idx: self.pick(idx, items))

    def pick(self, idx, items):
        if idx >= 0:
            command = items[idx].get("command")
            args = items[idx].get("args")
            self.view.window().run_command(command, args)




def canvas_parser(string, type):

    name = type
    print("name: ", name)
    items = string.split('<h3>')

    # Initiate Box properties.   Set as blank if undefined

    boxColour = snippets[type].get('Box-Colour','')
    print("boxColour: ", boxColour)
    titlePrefix = tP = snippets[type].get('Title-Prefix','')
    print("titlePrefix: ", titlePrefix)
    titleSuffix = snippets[type].get('Title-Suffix','')
    print("titleSuffix: ", titleSuffix)
    boxIcon = snippets[type].get('Box-Icon','')
    print("boxIcon: ", boxIcon)
    boxFooter = snippets[type].get('Box-Footer','')
    print("boxFooter: ", boxFooter)

    #if properties are defined, use these


    #if I am a Box
    if (type.startswith('Box-')):
        type = 'Box-Template'


    new_str = items[0] # Content prior to first <h3>
    # Create random ID
    # loop thorough items (as defind by <h3>)
    for idx, item in enumerate(items):
        i = str (idx)
        if idx == 0:
            # Built starting BS HTML
            new_str += snippets[type]['Start'].format(t=today,n=name)
            # If I have top level nav (V-tabs or H-tabs)
            if "Nav-Start" in snippets[type].keys():
                new_str += snippets[type]['Nav-Start'].format(n=name)
                for idx, item in enumerate(items):
                    i = str (idx)
                    sub_items = item.split('</h3>')
                    if idx > 0:
                        new_str += snippets[type]['Nav-Repeat'].format( i=i, a=sub_items[0],n=name)
                new_str += snippets[type]['Nav-End'].format()
        else:
            # Build repeating items
            sub_items = item.split('</h3>')

            # If heading text already starts with title prefix (for boxes etc)
            if (titlePrefix is not ''):
                print("sub_items[0]: ", sub_items[0])
                if(sub_items[0].startswith(titlePrefix)):
                    tP = ''
                else:
                    tP = titlePrefix + ' - '


            new_str += snippets[type]['Repeat'].format( i=i, a=sub_items[0], b=sub_items[1],bc=boxColour,bi=boxIcon,tp=tP,ts=titleSuffix,n=name,t=today,bf=boxFooter)
    new_str += snippets[type]['End'].format(t=today,n=name)

    # print("new_str: ", new_str)
    return new_str
