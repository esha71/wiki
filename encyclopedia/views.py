from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe

from . import util
from django import forms
import random
from markdown2 import Markdown


class EntryForm(forms.Form):
    page_name = forms.CharField(required=True, )
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 10, 'cols': 35}))

    # def __init__(self, *args, **kwargs):
    #     self.fields['page_name'].disabled = True
    #     super(EntryForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.page_name:


def index(request):
    entries =util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def newEntry(request):
    if request.method == 'POST':
         # save the page_name and description
        form = EntryForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            page = form.cleaned_data["page_name"]
            entry = util.get_entry(page)
            url_for_page = reverse('view_entry', args=[page])
            if not entry:
                util.save_entry(page, form.cleaned_data["description"])
                return HttpResponseRedirect(url_for_page)
            else:
                return render(request, "encyclopedia/error.html", {
                    "errorMsg": mark_safe(f"Page for <a href='{url_for_page}'>{page}</a> already exist"),
                })
        else:
            pass
    else:
        form = EntryForm(auto_id=False)
    return render(request, "encyclopedia/entryform.html", {
        "form": form
    })

def editEntry(request, page_name):
    if request.method == 'POST':
         # save the page_name and description
        form = EntryForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            page_name = form.cleaned_data["page_name"]
            # entry = util.get_entry(page_name)
            url_for_title = reverse('view_entry', args=[page_name])
            util.save_entry(page_name, form.cleaned_data["description"])
            return HttpResponseRedirect(url_for_title)
        else:
            return render(request, "encyclopedia/entryform.html", {
                "form": form
            })
    if page_name:
        description = util.get_entry(page_name)
        form = EntryForm(initial={"page_name":page_name, "description": description}, auto_id=False)
        form.fields['page_name'].widget.attrs['readonly'] = True

        return render(request, "encyclopedia/entryform.html", {
            "form": form
        })
    else:
        return render(request, "encyclopedia/notfound.html", {page_name: "No name provided"})

def search(request ):
    searchstring = request.GET.get('q')
    description = util.get_entry(searchstring)
    if description:
        return HttpResponseRedirect(reverse('view_entry', args=[searchstring]))
    else:
        titleList = util.list_entries()
        results = [title for title in titleList if searchstring.lower() in title.lower()]  #result = [element for element in data if element[1] == search]
        if results.__len__() > 0:
            return render(request, "encyclopedia/searchresults.html", {'search': results})
        # elif results.__len__() == 1:
        #     if searchstring.lower() == results[0].lower():
        #         return HttpResponseRedirect(reverse('view_entry', args=results))
        #     else:
        #         return render(request, "encyclopedia/searchresults.html", {'search': results})
        else:
            return render(request, "encyclopedia/error.html", {
                "errorMsg": f"your search for page_name '{searchstring}' was not found",
            })

def viewEntry(request, page_name):
    if page_name:
        description1 = util.get_entry(page_name)
        if description1:
            md = Markdown()
            description = md.convert(description1)
            return render(request, "encyclopedia/viewentry.html", {
                "page_name": page_name,
                "description": mark_safe(description),
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "errorMsg": f"your requested page '{page_name}' was not found",
            })
    else:
        return render(request, "encyclopedia/notfound.html", {page_name: "No details for page_name provided "})

def randomPageView(request):
    all_entries=util.list_entries()
    noOfEntries= len(all_entries)
    entry = random.randint(0, noOfEntries-1)
    selectEntryTitle=all_entries[entry]
    return HttpResponseRedirect(reverse('view_entry', args=[selectEntryTitle] ))
