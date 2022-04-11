var typingTimer = null
        var searchForm = $('.ad_list_get_form')
        var searchInput = searchForm.find("[name='q']")
        var searchShowBy = searchForm.find("[name='paginate_by']")
        var searchSortBy = searchForm.find("[name='sort_by']")
        var searchStartups = searchForm.find("[name='only_startups']")
        var searchCoFounders = $('#exampleRadios1')
        var searchEmployees = $('#exampleRadios2')
        var searchMin = searchForm.find("[name='min']")
        var searchMax = searchForm.find("[name='max']")
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
        searchCoFounders.change(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1)
        })
        searchEmployees.change(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1)
        })
        searchMin.keyup(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1000)
        })
        searchMax.keyup(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, 1000)
        })
        searchClearAll.change(function(event){
            window.location.href = '/ads/'
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
            if (searchCoFounders[0].checked){
                var only_who = searchCoFounders.val()
            } else if (searchEmployees[0].checked){
                var only_who = searchEmployees.val()
            } else {
                var only_who = 'no'
            }
            var min = searchMin.val()
            var max = searchMax.val()
            window.location.href = (
                '/ads/?q=' + query + 
                '&paginate_by=' + paginate_by +
                '&sort_by=' + sort_by +
                '&only_startups=' + startups +
                '&only_who=' + only_who +
                '&min=' + min +
                '&max=' + max)
        }