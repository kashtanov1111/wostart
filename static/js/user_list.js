var typingTimer = null
        var searchForm = $('.user_list_get_form')
        var searchInput = searchForm.find("[name='q']")
        var searchShowBy = searchForm.find("[name='paginate_by']")
        var searchSortBy = searchForm.find("[name='sort_by']")
        var searchStartups = searchForm.find("[name='only_startups']")
        var searchClearAll = searchForm.find("[name='clear_all']")

        searchInput.keyup(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1000)
        })
        searchInput.change(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1000)
        })
        searchShowBy.change(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1)
        })
        searchSortBy.change(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1)
        })
        searchStartups.change(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1)
        })
        searchClearAll.change(function(event){
            window.location.href = '/users/'
        })
        function performSearch(){
            var query = searchInput.val()
            var paginate_by = searchShowBy.val()
            var sort_by = searchSortBy.val()
            if (searchStartups[0].checked){
                startups = 'on'
            } else {
                startups = 'off'
            }
            window.location.href = (
                '/users/?q=' + query + 
                '&paginate_by=' + paginate_by +
                '&sort_by=' + sort_by +
                '&only_startups=' + startups)
        }