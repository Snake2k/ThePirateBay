# -*- coding: utf-8 -*- 
'''
The class definition of ThePirateBayFrame (TPBFrame)
'''
import wx
import tpb
import webbrowser

class TPBFrame (wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, 
                          title = u"The Pirate Bay", pos = wx.DefaultPosition, 
                          size = wx.Size(450, 560), 
                          style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        self.SetIcon(wx.Icon("thepiratebaylogo.png", wx.BITMAP_TYPE_PNG))
        self.TheBay = tpb.TPB("https://www.thepiratebay.sx")
        self.page = None
        self.maglinks = []
        self.urllinks = []
        self.currentitem = ""

        self.SetSizeHintsSz(wx.Size(450, 560), wx.Size(-1, -1))
        
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        
        self.m_panel1 = wx.Panel(self, wx.ID_ANY, 
                                 wx.DefaultPosition, wx.DefaultSize, 
                                 wx.TAB_TRAVERSAL)
        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        
        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.searchCtrl = wx.SearchCtrl(self.m_panel1, wx.ID_ANY, 
                                        wx.EmptyString, wx.DefaultPosition, 
                                        wx.DefaultSize, wx.TE_PROCESS_ENTER)
        self.searchCtrl.ShowSearchButton(True)
        self.searchCtrl.ShowCancelButton(False)
        bSizer3.Add(self.searchCtrl, 1, 
                    wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5)
        
        self.bSearch = wx.Button(self.m_panel1, wx.ID_ANY, 
                                 u"Search", wx.DefaultPosition, 
                                 wx.DefaultSize, 0)
        bSizer3.Add(self.bSearch, 0, wx.ALL, 5)
        
        bSizer2.Add(bSizer3, 0, wx.EXPAND, 5)
        
        bSizer4 = wx.BoxSizer(wx.VERTICAL)
        
        self.m_listCtrl1 = wx.ListCtrl(self.m_panel1, style=wx.LC_REPORT)

        self.m_listCtrl1.InsertColumn(0, "Name")
        self.m_listCtrl1.InsertColumn(1, "Size")
        self.m_listCtrl1.InsertColumn(2, "Seeders")
        self.m_listCtrl1.InsertColumn(3, "Leechers")
        
        self.m_listCtrl1.SetColumnWidth(0, 200)
        
        bSizer4.Add(self.m_listCtrl1, 1, wx.EXPAND|wx.ALL, 5)
        
        bSizer2.Add(bSizer4, 1, wx.EXPAND, 5)
        
        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        
        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.bPrev = wx.Button(self.m_panel1, wx.ID_ANY, 
                               u"Previous Page", wx.DefaultPosition, 
                               wx.DefaultSize, 0)
        self.bNext = wx.Button(self.m_panel1, wx.ID_ANY, 
                               u"Next Page", wx.DefaultPosition, 
                               wx.DefaultSize, 0)
        bSizer6.Add(self.bPrev, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5)
        bSizer6.Add(self.bNext, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5)
        
        bSizer5.Add(bSizer6, 1, wx.EXPAND, 5)

        self.bUrlOpen = wx.Button(self.m_panel1, wx.ID_ANY, 
                                  u"Visit Page", wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        self.bDownload = wx.Button(self.m_panel1, wx.ID_ANY,
                                   u"Download", wx.DefaultPosition,
                                   wx.DefaultSize, 0)

        bSizer5.Add(self.bUrlOpen, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5)
        bSizer5.Add(self.bDownload, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5)
        
        bSizer2.Add(bSizer5, 0, wx.EXPAND, 5)
        
        self.m_panel1.SetSizer(bSizer2)
        self.m_panel1.Layout()
        bSizer2.Fit(self.m_panel1)
        bSizer1.Add(self.m_panel1, 1, wx.EXPAND, 5)
        
        self.SetSizer(bSizer1)
        self.Layout()
        self.statusBar = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)
        self.menuBar = wx.MenuBar(0)
        self.mFile = wx.Menu()
        self.miClear = wx.MenuItem(self.mFile, wx.ID_ANY, 
                                   u"Clear", wx.EmptyString, wx.ITEM_NORMAL)
        self.mFile.AppendItem( self.miClear )
        
        self.mFile.AppendSeparator()
        
        self.miClose = wx.MenuItem(self.mFile, wx.ID_ANY, 
                                   u"Close", wx.EmptyString, wx.ITEM_NORMAL)
        self.mFile.AppendItem(self.miClose)
        
        self.menuBar.Append(self.mFile, u"File") 
        
        self.mEdit = wx.Menu()
        self.miPref = wx.MenuItem(self.mEdit, wx.ID_ANY, 
                                  u"Preferences", wx.EmptyString, wx.ITEM_NORMAL)
        self.mEdit.AppendItem(self.miPref)
        
        self.menuBar.Append(self.mEdit, u"Edit") 
        
        self.mHelp = wx.Menu()
        self.miAbout = wx.MenuItem(self.mHelp, wx.ID_ANY, 
                                   u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.mHelp.AppendItem(self.miAbout)
        
        self.menuBar.Append(self.mHelp, u"Help") 
        
        self.SetMenuBar(self.menuBar)
        
        self.Centre(wx.BOTH)

        self.bNext.Disable()
        self.bPrev.Disable()
        self.bUrlOpen.Disable()
        self.bDownload.Disable()

        self.bNext.SetToolTipString("Go to the next search page.")
        self.bPrev.SetToolTipString("Go to the previous search page.")
        self.bUrlOpen.SetToolTipString("Visit the webpage " + \
                                       "of the selected torrent.")
        self.bDownload.SetToolTipString("Download the selected torrent.")
        self.bSearch.SetToolTipString("Search for torrent links.")

        # Events
        self.searchCtrl.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self._search)
        self.searchCtrl.Bind(wx.EVT_TEXT_ENTER, self._search)
        self.bSearch.Bind(wx.EVT_BUTTON, self._search)
        self.bPrev.Bind(wx.EVT_BUTTON, self._prevpage)
        self.bNext.Bind(wx.EVT_BUTTON, self._nextpage)
        self.bDownload.Bind(wx.EVT_BUTTON, self._download)
        self.bUrlOpen.Bind(wx.EVT_BUTTON, self._urlopen)
        self.Bind(wx.EVT_MENU, self._clear, id = self.miClear.GetId())
        self.Bind(wx.EVT_MENU, self._close, id = self.miClose.GetId())
        self.Bind(wx.EVT_MENU, self._showpref, id = self.miPref.GetId())
        self.Bind(wx.EVT_MENU, self._showabout, id = self.miAbout.GetId())
 
    def _search(self, event):
        '''
        This method gets the text from the search ctrl
        and queries it via TPB Api and fetches the results into
        the listctrl.
        '''
        self._refreshlinks()
        self.m_listCtrl1.DeleteAllItems()
        self.m_listCtrl1.Refresh()
        itemsearched = self.searchCtrl.GetValue()
        if self.page == None or self.currentitem != itemsearched:
            self.page = 1
            self.bNext.Enable()
            self.bDownload.Enable()
            self.bUrlOpen.Enable()
            self.currentitem = itemsearched
        elif self.page == 1:
            self.bPrev.Disable()
        elif self.page > 1:
            self.bPrev.Enable()
        search = self.TheBay.search(itemsearched, 
                                    order = tpb.ORDERS.SEEDERS, 
                                    category = tpb.CATEGORIES.ALL)
        text = "Fetching results for \"%s\" (Page #%d)" % (itemsearched, 
                                                           self.page)
        self.statusBar.SetStatusText(text)
        for item in search.page(self.page):
            itemindex = self.m_listCtrl1.GetItemCount()
            self.m_listCtrl1.InsertStringItem(itemindex, str(item.title))
            self.m_listCtrl1.SetStringItem(itemindex, 1, str(item.size))
            self.m_listCtrl1.SetStringItem(itemindex, 2, str(item.seeders))
            self.m_listCtrl1.SetStringItem(itemindex, 3, str(item.leechers))
            self.maglinks.append(str(item.magnet_link))
            self.urllinks.append(str(item.url))
        text = "Done. Displaying results for \"%s\" (Page #%d)" % (itemsearched,
                                                                   self.page)
        self.statusBar.SetStatusText(text)

    def _prevpage(self, event):
        '''
        Goes to the previous page if page number is not 1,
        else, it stays disabled.
        '''
        self.page -= 1
        self._search(event)
    
    def _nextpage(self, event):
        '''
        Goes to the next page if page number + 1 exists,
        else, is disabled.
        '''
        self.page += 1
        self._search(event)

    def _refreshlinks(self):
        self.urllinks = []
        self.maglinks = []
    
    def _clear(self, event):
        '''
        Clears the current results in the listctrl and refreshes the
        TBP connector.
        '''
        self._refreshlinks()
        self.m_listCtrl1.DeleteAllItems()
        self.page = None
        self.searchCtrl.Clear()
        self.bNext.Disable()
        self.bPrev.Disable()
        self.bDownload.Disable()
        self.bUrlOpen.Disable()
        self.statusBar.SetStatusText("Application Cleared.")
    
    def _close(self, event):
        '''
        Closes the window lol
        '''
        self.Close()

    def _download(self, event):
        '''
        Presents the magnetic link of selected item as a hyperlink.
        '''
        selected = [] 
        item = self.m_listCtrl1.GetFirstSelected() 
        while item != -1: 
            selected.append(item) 
            item = self.m_listCtrl1.GetNextSelected(item) 
        if len(selected) == 0:
            wx.MessageBox("Please select an item to download.", 
                          "Download", wx.OK | wx.ICON_EXCLAMATION)
        else:
            link = self.maglinks[selected[0]]
            webbrowser.open(link)

    def _urlopen(self, event):
        '''
        Presents the url for the selected item as a hyperlink.
        '''
        selected = [] 
        item = self.m_listCtrl1.GetFirstSelected() 
        while item != -1: 
            selected.append(item) 
            item = self.m_listCtrl1.GetNextSelected(item) 
        if len(selected) == 0:
            wx.MessageBox("Please select an item to visit page.", 
                          "Download", wx.OK | wx.ICON_EXCLAMATION)
        else:
            link = self.urllinks[selected[0]]
            wx.MessageBox("Not completely implemented.","Visit Page",
                          wx.OK | wx.ICON_EXCLAMATION)
            #webbrowser.open(link)

    def _showpref(self, event):
        '''
        Shows the preference menu,
        It is not implemented,
        Hopefully, I can implement a way to allow users to freely
        configure the output as they wish to see it.
        '''
        wx.MessageBox("The Preferences Menu has not been implemented." + \
                      "\nSorry :'(", "Preferences", wx.OK | wx.ICON_ERROR)
    
    def _showabout(self, event):
        '''
        Shows the about message.
        '''
        wx.MessageBox("The Unofficial Desktop Client for The Pirate Bay." + \
                      "\nImplemented using wxPython and " + \
                      "ThePirateBay API (Unofficial).\n" + \
                      "Links:\nTPB API: https://github.com/thekarangoel/TPB" + \
                      "\nwxPython: http://www.wxpython.org/", "About",
                      wx.OK | wx.ICON_INFORMATION)
