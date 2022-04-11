var typingTimer = null
        var searchForm = $('.response_list_get_form')
        var searchShowBy = searchForm.find("[name='paginate_by']")
        var searchSortBy = searchForm.find("[name='sort_by']")
        var searchAds = searchForm.find("[name='ads']")
        var searchClearAll = searchForm.find("[name='clear_all']")

        searchShowBy.change(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1)
        })
        searchSortBy.change(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1)
        })
        searchAds.change(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1)
        })
        searchClearAll.change(function(event){
            window.location.href = '/responses/'
        })
        function performSearch(){
            var paginate_by = searchShowBy.val()
            var sort_by = searchSortBy.val()
            var ad = searchAds.val()
            window.location.href = (
                '/responses/?' +
                'paginate_by=' + paginate_by +
                '&sort_by=' + sort_by +
                '&ads=' + ad)
        }