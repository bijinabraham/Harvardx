from django.shortcuts import render
from random import random, choice
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown2
from django import forms
from django.views.defaults import page_not_found


class NewEntryForm(forms.Form):
    Title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), label="Title")
    Content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), label="Content")


class EntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    content = forms.CharField(widget=forms.Textarea(), label="Entry Content")

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if title.lower() in [x.lower() for x in util.list_entries()]:
    #         raise forms.ValidationError("You already have such entry!")
    #     return title


# convert md to html format
md = markdown2.Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# create new page


def new(request):
    form = NewEntryForm(request.POST)
    EntryPresent = None
    if request.method == "POST":
        if form.is_valid():
            entries = util.list_entries()
            for entry in entries:
                if(form.cleaned_data["Title"].lower() == entry.lower()):
                    EntryPresent = True
                    errmsg = "The Title Entered Already Exists."
                    types = "danger"
                    return render(request, "encyclopedia/new.html", {
                        "form": form,
                        "types": types,
                        "errmsg": errmsg
                    })

            if EntryPresent != True:
                title = form.cleaned_data["Title"]
                content = form.cleaned_data["Content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(form.cleaned_data["Title"])

            else:
                return render(request, "encyclopedia/new.html", {
                    "form": form})

    types = "warning"
    errmsg = "Please check your data for errors before submitting"
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm(),
        "types": types,
        "errmsg": errmsg
    })


# random entry


def getrandompage(request):
    items = choice(util.list_entries())
    randomitem = util.get_entry(items)
    return render(request, "encyclopedia/view.html", {
        "title": items,
        "entries": md.convert(randomitem)
    })

# for navigating from home and url


def greet(request, title):
    if not util.get_entry(title):
        return page_not_found(request, True, template_name="404.html")
    return render(request, "encyclopedia/view.html", {
        "entries": md.convert(util.get_entry(title)),
        "title": title,
        "greet": True
    })

# search bar


def searchstr(request):
    entries = util.list_entries()
    find_entries = list()
    search_box = request.POST.get("search")
    lista = [x.lower() for x in entries]
    if search_box.lower() in lista:
        search_boxs = util.get_entry(search_box)
        return render(request, "encyclopedia/view.html", {
            "title": search_box,
            "entries": md.convert(search_boxs)
        })
        # return HttpResponseRedirect(f"{search_box}")

# find substring
    for entry in entries:
        if search_box.lower() in entry.lower():
            find_entries.append(entry)
        else:
            print(f'{find_entries}')

    if find_entries:
        return render(request, "encyclopedia/search.html", {
            "search_result": find_entries,
            "search": search_box
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "no_result": f"No results for \"{search_box}\""
        })

# edit page


def edit(request, title=None):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if not title:
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
            else:
                return render(request, "encyclopedia/edit.html", {
                    "form": form
                })
        elif title == form.data['title']:
            title = form.data['title']
            content = form.data['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('wiki:greet', args=[title]))
    if not title:
        return render(request, "encyclopedia/edit.html", {
            "form": EntryForm()
        })
    data = {'title': title, 'content': util.get_entry(title)}
    populated_form = EntryForm(initial=data)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": populated_form,
        "edit": True
    })
