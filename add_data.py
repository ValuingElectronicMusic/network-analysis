




<!DOCTYPE html>
<html class="   ">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    
    <title>network-analysis/add_data.py at db232c18660cc781c5e4ed902480e42522cc70d6 · ValuingElectronicMusic/network-analysis · GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png" />
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png" />
    <meta property="fb:app_id" content="1401488693436528"/>

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="ValuingElectronicMusic/network-analysis" name="twitter:title" /><meta content="network-analysis - Code for exploring the value of electronic music via analysing network interactions on Soundcloud." name="twitter:description" /><meta content="https://avatars3.githubusercontent.com/u/6595936?s=400" name="twitter:image:src" />
<meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://avatars3.githubusercontent.com/u/6595936?s=400" property="og:image" /><meta content="ValuingElectronicMusic/network-analysis" property="og:title" /><meta content="https://github.com/ValuingElectronicMusic/network-analysis" property="og:url" /><meta content="network-analysis - Code for exploring the value of electronic music via analysing network interactions on Soundcloud." property="og:description" />

    <link rel="assets" href="https://github.global.ssl.fastly.net/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035/">
    <link rel="xhr-socket" href="/_sockets" />

    <meta name="msapplication-TileImage" content="/windows-tile.png" />
    <meta name="msapplication-TileColor" content="#ffffff" />
    <meta name="selected-link" value="repo_source" data-pjax-transient />
    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="8949AC64:5DB6:14E4DD1:533D62EA" name="octolytics-dimension-request_id" />
    

    
    
    <link rel="icon" type="image/x-icon" href="https://github.global.ssl.fastly.net/favicon.ico" />

    <meta content="authenticity_token" name="csrf-param" />
<meta content="M1Q0KEP7BHXBAGudt+HCCf//x35Lp3bSo9GbXNyTLCA=" name="csrf-token" />

    <link href="https://github.global.ssl.fastly.net/assets/github-a3b47dba0079fcdc34bf0126746f9827ade6f76f.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://github.global.ssl.fastly.net/assets/github2-db8f6f9bbe1b0e611d0e24fc905420b0c99729f2.css" media="all" rel="stylesheet" type="text/css" />
    


        <script crossorigin="anonymous" src="https://github.global.ssl.fastly.net/assets/frameworks-dca097f6f454ee06b43ea4817a154392e3caf824.js" type="text/javascript"></script>
        <script async="async" crossorigin="anonymous" src="https://github.global.ssl.fastly.net/assets/github-50a9b02be7b7235510a2895ac6ebed3f2a85a55f.js" type="text/javascript"></script>
        
        
      <meta http-equiv="x-pjax-version" content="5fc927f2f0bc01ddd7083de2731490da">

        <link data-pjax-transient rel='permalink' href='/ValuingElectronicMusic/network-analysis/blob/db232c18660cc781c5e4ed902480e42522cc70d6/add_data.py'>

  <meta name="description" content="network-analysis - Code for exploring the value of electronic music via analysing network interactions on Soundcloud." />

  <meta content="6595936" name="octolytics-dimension-user_id" /><meta content="ValuingElectronicMusic" name="octolytics-dimension-user_login" /><meta content="16548276" name="octolytics-dimension-repository_id" /><meta content="ValuingElectronicMusic/network-analysis" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="16548276" name="octolytics-dimension-repository_network_root_id" /><meta content="ValuingElectronicMusic/network-analysis" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/ValuingElectronicMusic/network-analysis/commits/db232c18660cc781c5e4ed902480e42522cc70d6.atom" rel="alternate" title="Recent Commits to network-analysis:db232c18660cc781c5e4ed902480e42522cc70d6" type="application/atom+xml" />

  </head>


  <body class="logged_out  env-production windows vis-public page-blob">
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>
    <div class="wrapper">
      
      
      
      


      
      <div class="header header-logged-out">
  <div class="container clearfix">

    <a class="header-logo-wordmark" href="https://github.com/">
      <span class="mega-octicon octicon-logo-github"></span>
    </a>

    <div class="header-actions">
        <a class="button primary" href="/join">Sign up</a>
      <a class="button signin" href="/login?return_to=%2FValuingElectronicMusic%2Fnetwork-analysis%2Fblob%2Fdb232c18660cc781c5e4ed902480e42522cc70d6%2Fadd_data.py">Sign in</a>
    </div>

    <div class="command-bar js-command-bar  in-repository">

      <ul class="top-nav">
          <li class="explore"><a href="/explore">Explore</a></li>
        <li class="features"><a href="/features">Features</a></li>
          <li class="enterprise"><a href="https://enterprise.github.com/">Enterprise</a></li>
          <li class="blog"><a href="/blog">Blog</a></li>
      </ul>
        <form accept-charset="UTF-8" action="/search" class="command-bar-form" id="top_search_form" method="get">

<div class="commandbar">
  <span class="message"></span>
  <input type="text" data-hotkey="/ s" name="q" id="js-command-bar-field" placeholder="Search or type a command" tabindex="1" autocapitalize="off"
    
    
      data-repo="ValuingElectronicMusic/network-analysis"
      data-branch="db232c18660cc781c5e4ed902480e42522cc70d6"
      data-sha="278c9047e417ad79fd78dc3f7fa3232c99e9ba5d"
  >
  <div class="display hidden"></div>
</div>

    <input type="hidden" name="nwo" value="ValuingElectronicMusic/network-analysis" />

    <div class="select-menu js-menu-container js-select-menu search-context-select-menu">
      <span class="minibutton select-menu-button js-menu-target" role="button" aria-haspopup="true">
        <span class="js-select-button">This repository</span>
      </span>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container" aria-hidden="true">
        <div class="select-menu-modal">

          <div class="select-menu-item js-navigation-item js-this-repository-navigation-item selected">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" class="js-search-this-repository" name="search_target" value="repository" checked="checked" />
            <div class="select-menu-item-text js-select-button-text">This repository</div>
          </div> <!-- /.select-menu-item -->

          <div class="select-menu-item js-navigation-item js-all-repositories-navigation-item">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" name="search_target" value="global" />
            <div class="select-menu-item-text js-select-button-text">All repositories</div>
          </div> <!-- /.select-menu-item -->

        </div>
      </div>
    </div>

  <span class="help tooltipped tooltipped-s" aria-label="Show command bar help">
    <span class="octicon octicon-question"></span>
  </span>


  <input type="hidden" name="ref" value="cmdform">

</form>
    </div>

  </div>
</div>



      <div id="start-of-content" class="accessibility-aid"></div>
          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        

<ul class="pagehead-actions">


  <li>
    <a href="/login?return_to=%2FValuingElectronicMusic%2Fnetwork-analysis"
    class="minibutton with-count js-toggler-target star-button tooltipped tooltipped-n"
    aria-label="You must be signed in to star a repository" rel="nofollow">
    <span class="octicon octicon-star"></span>Star
  </a>

    <a class="social-count js-social-count" href="/ValuingElectronicMusic/network-analysis/stargazers">
      0
    </a>

  </li>

    <li>
      <a href="/login?return_to=%2FValuingElectronicMusic%2Fnetwork-analysis"
        class="minibutton with-count js-toggler-target fork-button tooltipped tooltipped-n"
        aria-label="You must be signed in to fork a repository" rel="nofollow">
        <span class="octicon octicon-git-branch"></span>Fork
      </a>
      <a href="/ValuingElectronicMusic/network-analysis/network" class="social-count">
        1
      </a>
    </li>
</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="repo-label"><span>public</span></span>
          <span class="mega-octicon octicon-repo"></span>
          <span class="author">
            <a href="/ValuingElectronicMusic" class="url fn" itemprop="url" rel="author"><span itemprop="title">ValuingElectronicMusic</span></a>
          </span>
          <span class="repohead-name-divider">/</span>
          <strong><a href="/ValuingElectronicMusic/network-analysis" class="js-current-repository js-repo-home-link">network-analysis</a></strong>

          <span class="page-context-loader">
            <img alt="Octocat-spinner-32" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">
      <div class="repository-with-sidebar repo-container new-discussion-timeline js-new-discussion-timeline  ">
        <div class="repository-sidebar clearfix">
            

<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped tooltipped-w" aria-label="Code">
        <a href="/ValuingElectronicMusic/network-analysis" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-gotokey="c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_tags repo_branches /ValuingElectronicMusic/network-analysis">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

        <li class="tooltipped tooltipped-w" aria-label="Issues">
          <a href="/ValuingElectronicMusic/network-analysis/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="i" data-selected-links="repo_issues /ValuingElectronicMusic/network-analysis/issues">
            <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>

      <li class="tooltipped tooltipped-w" aria-label="Pull Requests">
        <a href="/ValuingElectronicMusic/network-analysis/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="p" data-selected-links="repo_pulls /ValuingElectronicMusic/network-analysis/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped tooltipped-w" aria-label="Pulse">
        <a href="/ValuingElectronicMusic/network-analysis/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /ValuingElectronicMusic/network-analysis/pulse">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped tooltipped-w" aria-label="Graphs">
        <a href="/ValuingElectronicMusic/network-analysis/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /ValuingElectronicMusic/network-analysis/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped tooltipped-w" aria-label="Network">
        <a href="/ValuingElectronicMusic/network-analysis/network" aria-label="Network" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-selected-links="repo_network /ValuingElectronicMusic/network-analysis/network">
          <span class="octicon octicon-git-branch"></span> <span class="full-word">Network</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


  </div>
</div>

              <div class="only-with-full-nav">
                

  

<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><strong>HTTPS</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/ValuingElectronicMusic/network-analysis.git" readonly="readonly">

    <span aria-label="copy to clipboard" class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/ValuingElectronicMusic/network-analysis.git" data-copied-hint="copied!"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><strong>Subversion</strong> checkout URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/ValuingElectronicMusic/network-analysis" readonly="readonly">

    <span aria-label="copy to clipboard" class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/ValuingElectronicMusic/network-analysis" data-copied-hint="copied!"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <span class="help tooltipped tooltipped-n" aria-label="Get help on which URL is right for you.">
    <a href="https://help.github.com/articles/which-remote-url-should-i-use">
    <span class="octicon octicon-question"></span>
    </a>
  </span>
</p>


  <a href="http://windows.github.com" class="minibutton sidebar-button" title="Save ValuingElectronicMusic/network-analysis to your computer and use it in GitHub Desktop." aria-label="Save ValuingElectronicMusic/network-analysis to your computer and use it in GitHub Desktop.">
    <span class="octicon octicon-device-desktop"></span>
    Clone in Desktop
  </a>

                <a href="/ValuingElectronicMusic/network-analysis/archive/db232c18660cc781c5e4ed902480e42522cc70d6.zip"
                   class="minibutton sidebar-button"
                   aria-label="Download ValuingElectronicMusic/network-analysis as a zip file"
                   title="Download ValuingElectronicMusic/network-analysis as a zip file"
                   rel="nofollow">
                  <span class="octicon octicon-cloud-download"></span>
                  Download ZIP
                </a>
              </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          


<!-- blob contrib key: blob_contributors:v21:401b2d47e63096fe5a85b38eb45bb6ff -->

<p title="This is a placeholder element" class="js-history-link-replace hidden"></p>

<a href="/ValuingElectronicMusic/network-analysis/find/db232c18660cc781c5e4ed902480e42522cc70d6" data-pjax data-hotkey="t" class="js-show-file-finder" style="display:none">Show File Finder</a>

<div class="file-navigation">
  

<div class="select-menu js-menu-container js-select-menu" >
  <span class="minibutton select-menu-button js-menu-target" data-hotkey="w"
    data-master-branch="master"
    data-ref=""
    role="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <span class="octicon octicon-git-branch"></span>
    <i>tree:</i>
    <span class="js-select-button">db232c1866</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-remove-close js-menu-close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/ValuingElectronicMusic/network-analysis/blob/master/add_data.py"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/ValuingElectronicMusic/network-analysis/tree/db232c18660cc781c5e4ed902480e42522cc70d6" data-branch="db232c18660cc781c5e4ed902480e42522cc70d6" data-direction="back" data-pjax="true" itemscope="url" rel="nofollow"><span itemprop="title">network-analysis</span></a></span></span><span class="separator"> / </span><strong class="final-path">add_data.py</strong> <span aria-label="copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="add_data.py" data-copied-hint="copied!"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


  <div class="commit file-history-tease">
    <img alt="daniel-allington" class="main-avatar js-avatar" data-user="6640474" height="24" src="https://avatars3.githubusercontent.com/u/6640474?s=140" width="24" />
    <span class="author"><a href="/daniel-allington" rel="author">daniel-allington</a></span>
    <time class="js-relative-date" data-title-format="YYYY-MM-DD HH:mm:ss" datetime="2014-04-02T10:25:41+01:00" title="2014-04-02 10:25:41">April 02, 2014</time>
    <div class="commit-title">
        <a href="/ValuingElectronicMusic/network-analysis/commit/db232c18660cc781c5e4ed902480e42522cc70d6" class="message" data-pjax="true" title="Small change to comments

Something else to fix soon.">Small change to comments</a>
    </div>

    <div class="participation">
      <p class="quickstat"><a href="#blob_contributors_box" rel="facebox"><strong>1</strong>  contributor</a></p>
      
    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img alt="daniel-allington" class=" js-avatar" data-user="6640474" height="24" src="https://avatars3.githubusercontent.com/u/6640474?s=140" width="24" />
            <a href="/daniel-allington">daniel-allington</a>
          </li>
      </ul>
    </div>
  </div>

<div class="file-box">
  <div class="file">
    <div class="meta clearfix">
      <div class="info file-name">
        <span class="icon"><b class="octicon octicon-file-text"></b></span>
        <span class="mode" title="File Mode">file</span>
        <span class="meta-divider"></span>
          <span>139 lines (101 sloc)</span>
          <span class="meta-divider"></span>
        <span>4.353 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
              <a class="minibutton disabled tooltipped tooltipped-w" href="#"
                 aria-label="You must be signed in to make or propose changes">Edit</a>
          <a href="/ValuingElectronicMusic/network-analysis/raw/db232c18660cc781c5e4ed902480e42522cc70d6/add_data.py" class="button minibutton " id="raw-url">Raw</a>
            <a href="/ValuingElectronicMusic/network-analysis/blame/db232c18660cc781c5e4ed902480e42522cc70d6/add_data.py" class="button minibutton js-update-url-with-hash">Blame</a>
          <a href="/ValuingElectronicMusic/network-analysis/commits/db232c18660cc781c5e4ed902480e42522cc70d6/add_data.py" class="button minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->
          <a class="minibutton danger disabled empty-icon tooltipped tooltipped-w" href="#"
             aria-label="You must be signed in to make or propose changes">
          Delete
        </a>
      </div><!-- /.actions -->
    </div>
        <div class="blob-wrapper data type-python js-blob-data">
        <table class="file-code file-diff tab-size-8">
          <tr class="file-code-line">
            <td class="blob-line-nums">
              <span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>
<span id="L43" rel="#L43">43</span>
<span id="L44" rel="#L44">44</span>
<span id="L45" rel="#L45">45</span>
<span id="L46" rel="#L46">46</span>
<span id="L47" rel="#L47">47</span>
<span id="L48" rel="#L48">48</span>
<span id="L49" rel="#L49">49</span>
<span id="L50" rel="#L50">50</span>
<span id="L51" rel="#L51">51</span>
<span id="L52" rel="#L52">52</span>
<span id="L53" rel="#L53">53</span>
<span id="L54" rel="#L54">54</span>
<span id="L55" rel="#L55">55</span>
<span id="L56" rel="#L56">56</span>
<span id="L57" rel="#L57">57</span>
<span id="L58" rel="#L58">58</span>
<span id="L59" rel="#L59">59</span>
<span id="L60" rel="#L60">60</span>
<span id="L61" rel="#L61">61</span>
<span id="L62" rel="#L62">62</span>
<span id="L63" rel="#L63">63</span>
<span id="L64" rel="#L64">64</span>
<span id="L65" rel="#L65">65</span>
<span id="L66" rel="#L66">66</span>
<span id="L67" rel="#L67">67</span>
<span id="L68" rel="#L68">68</span>
<span id="L69" rel="#L69">69</span>
<span id="L70" rel="#L70">70</span>
<span id="L71" rel="#L71">71</span>
<span id="L72" rel="#L72">72</span>
<span id="L73" rel="#L73">73</span>
<span id="L74" rel="#L74">74</span>
<span id="L75" rel="#L75">75</span>
<span id="L76" rel="#L76">76</span>
<span id="L77" rel="#L77">77</span>
<span id="L78" rel="#L78">78</span>
<span id="L79" rel="#L79">79</span>
<span id="L80" rel="#L80">80</span>
<span id="L81" rel="#L81">81</span>
<span id="L82" rel="#L82">82</span>
<span id="L83" rel="#L83">83</span>
<span id="L84" rel="#L84">84</span>
<span id="L85" rel="#L85">85</span>
<span id="L86" rel="#L86">86</span>
<span id="L87" rel="#L87">87</span>
<span id="L88" rel="#L88">88</span>
<span id="L89" rel="#L89">89</span>
<span id="L90" rel="#L90">90</span>
<span id="L91" rel="#L91">91</span>
<span id="L92" rel="#L92">92</span>
<span id="L93" rel="#L93">93</span>
<span id="L94" rel="#L94">94</span>
<span id="L95" rel="#L95">95</span>
<span id="L96" rel="#L96">96</span>
<span id="L97" rel="#L97">97</span>
<span id="L98" rel="#L98">98</span>
<span id="L99" rel="#L99">99</span>
<span id="L100" rel="#L100">100</span>
<span id="L101" rel="#L101">101</span>
<span id="L102" rel="#L102">102</span>
<span id="L103" rel="#L103">103</span>
<span id="L104" rel="#L104">104</span>
<span id="L105" rel="#L105">105</span>
<span id="L106" rel="#L106">106</span>
<span id="L107" rel="#L107">107</span>
<span id="L108" rel="#L108">108</span>
<span id="L109" rel="#L109">109</span>
<span id="L110" rel="#L110">110</span>
<span id="L111" rel="#L111">111</span>
<span id="L112" rel="#L112">112</span>
<span id="L113" rel="#L113">113</span>
<span id="L114" rel="#L114">114</span>
<span id="L115" rel="#L115">115</span>
<span id="L116" rel="#L116">116</span>
<span id="L117" rel="#L117">117</span>
<span id="L118" rel="#L118">118</span>
<span id="L119" rel="#L119">119</span>
<span id="L120" rel="#L120">120</span>
<span id="L121" rel="#L121">121</span>
<span id="L122" rel="#L122">122</span>
<span id="L123" rel="#L123">123</span>
<span id="L124" rel="#L124">124</span>
<span id="L125" rel="#L125">125</span>
<span id="L126" rel="#L126">126</span>
<span id="L127" rel="#L127">127</span>
<span id="L128" rel="#L128">128</span>
<span id="L129" rel="#L129">129</span>
<span id="L130" rel="#L130">130</span>
<span id="L131" rel="#L131">131</span>
<span id="L132" rel="#L132">132</span>
<span id="L133" rel="#L133">133</span>
<span id="L134" rel="#L134">134</span>
<span id="L135" rel="#L135">135</span>
<span id="L136" rel="#L136">136</span>
<span id="L137" rel="#L137">137</span>
<span id="L138" rel="#L138">138</span>

            </td>
            <td class="blob-line-code"><div class="code-body highlight"><pre><div class='line' id='LC1'><span class="sd">&#39;&#39;&#39;</span></div><div class='line' id='LC2'><span class="sd">Created on Apr 1, 2014</span></div><div class='line' id='LC3'><br/></div><div class='line' id='LC4'><span class="sd">@author: daniel-allington</span></div><div class='line' id='LC5'><span class="sd">&#39;&#39;&#39;</span></div><div class='line' id='LC6'><br/></div><div class='line' id='LC7'><span class="kn">import</span> <span class="nn">sqlite3</span></div><div class='line' id='LC8'><span class="kn">import</span> <span class="nn">string</span></div><div class='line' id='LC9'><br/></div><div class='line' id='LC10'><br/></div><div class='line' id='LC11'><span class="c"># Strings used for creating tables. Note that I&#39;ve removed the primary</span></div><div class='line' id='LC12'><span class="c"># keys because they didn&#39;t seem to work properly and I didn&#39;t have time</span></div><div class='line' id='LC13'><span class="c"># to fix them. But with the code packaged up in single functions as below</span></div><div class='line' id='LC14'><span class="c"># I&#39;m hopeful it will only need to be fixed once!</span></div><div class='line' id='LC15'><br/></div><div class='line' id='LC16'><span class="n">dummy_table_creator</span><span class="o">=</span><span class="s">&#39;id INTEGER, user_id INTEGER, title TEXT&#39;</span></div><div class='line' id='LC17'><br/></div><div class='line' id='LC18'><span class="n">tracks_table_creator</span><span class="o">=</span><span class="s">&#39;&#39;&#39;id INTEGER, user_id INTEGER, title TEXT,</span></div><div class='line' id='LC19'><span class="s">permalink_url TEXT,  track_type TEXT, state TEXT, created_at TEXT,</span></div><div class='line' id='LC20'><span class="s">original_format TEXT, description TEXT, sharing TEXT,</span></div><div class='line' id='LC21'><span class="s">genre TEXT, duration INTEGER, key_signature TEXT, bpm INTEGER,</span></div><div class='line' id='LC22'><span class="s">license TEXT, label_name TEXT,</span></div><div class='line' id='LC23'><span class="s">favoritings_count INTEGER,</span></div><div class='line' id='LC24'><span class="s">streamable TEXT, stream_url TEXT,</span></div><div class='line' id='LC25'><span class="s">downloadable TEXT, download_count INTEGER,</span></div><div class='line' id='LC26'><span class="s">commentable TEXT,</span></div><div class='line' id='LC27'><span class="s">purchase_url TEXT, artwork_url TEXT, video_url TEXT, embeddable_by TEXT,</span></div><div class='line' id='LC28'><span class="s">release TEXT, release_month INTEGER, release_day INTEGER, release_year INTEGER,</span></div><div class='line' id='LC29'><span class="s">tag_list TEXT&#39;&#39;&#39;</span></div><div class='line' id='LC30'><br/></div><div class='line' id='LC31'><span class="n">users_table_creator</span><span class="o">=</span><span class="s">&#39;&#39;&#39;id INTEGER, username TEXT, </span></div><div class='line' id='LC32'><span class="s">permalink_url TEXT, full_name TEXT, description TEXT,  </span></div><div class='line' id='LC33'><span class="s">city TEXT, country TEXT, </span></div><div class='line' id='LC34'><span class="s">track_count INTEGER, playlist_count INTEGER, </span></div><div class='line' id='LC35'><span class="s">followers_count INTEGER, followings_count INTEGER, </span></div><div class='line' id='LC36'><span class="s">public_favorites_count INTEGER&#39;&#39;&#39;</span></div><div class='line' id='LC37'><br/></div><div class='line' id='LC38'><span class="n">x_follows_y_table_creator</span><span class="o">=</span><span class="s">&#39;follower INTEGER, followed INTEGER&#39;</span></div><div class='line' id='LC39'><br/></div><div class='line' id='LC40'><span class="n">groups_table_creator</span><span class="o">=</span><span class="s">&#39;user_id INTEGER, group_id INTEGER&#39;</span></div><div class='line' id='LC41'><br/></div><div class='line' id='LC42'><span class="n">favourites_table_creator</span><span class="o">=</span><span class="s">&#39;user INTEGER, track INTEGER&#39;</span></div><div class='line' id='LC43'><br/></div><div class='line' id='LC44'><span class="n">comments_table_creator</span><span class="o">=</span><span class="s">&#39;&#39;&#39;id INTEGER,</span></div><div class='line' id='LC45'><span class="s">body TEXT, user_id INTEGER, track_id INTEGER, </span></div><div class='line' id='LC46'><span class="s">timestamp INTEGER, created_at TEXT)&#39;&#39;&#39;</span></div><div class='line' id='LC47'><br/></div><div class='line' id='LC48'><br/></div><div class='line' id='LC49'><span class="c"># Generalised function for creating each of the tables we need, using</span></div><div class='line' id='LC50'><span class="c"># the above strings</span></div><div class='line' id='LC51'><br/></div><div class='line' id='LC52'><span class="k">def</span> <span class="nf">create_table</span><span class="p">(</span><span class="n">cursor</span><span class="p">,</span><span class="n">table</span><span class="p">,</span><span class="n">table_creator</span><span class="p">):</span></div><div class='line' id='LC53'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cursor</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span><span class="s">&#39;DROP TABLE IF EXISTS {}&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">table</span><span class="p">))</span></div><div class='line' id='LC54'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cursor</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span><span class="s">&#39;CREATE TABLE IF NOT &#39;</span></div><div class='line' id='LC55'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;EXISTS {}({})&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">table</span><span class="p">,</span><span class="n">table_creator</span><span class="p">))</span></div><div class='line' id='LC56'><br/></div><div class='line' id='LC57'><br/></div><div class='line' id='LC58'><span class="c"># Functions for turning table-creating strings (above) into lists of</span></div><div class='line' id='LC59'><span class="c"># attributes</span></div><div class='line' id='LC60'><br/></div><div class='line' id='LC61'><span class="k">def</span> <span class="nf">att_string</span><span class="p">(</span><span class="nb">str</span><span class="p">):</span></div><div class='line' id='LC62'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nb">str</span><span class="o">.</span><span class="n">translate</span><span class="p">(</span><span class="bp">None</span><span class="p">,</span><span class="n">string</span><span class="o">.</span><span class="n">ascii_uppercase</span><span class="p">)</span></div><div class='line' id='LC63'><br/></div><div class='line' id='LC64'><br/></div><div class='line' id='LC65'><span class="k">def</span> <span class="nf">att_list</span><span class="p">(</span><span class="n">att_str</span><span class="p">):</span></div><div class='line' id='LC66'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="p">[</span><span class="n">att</span><span class="o">.</span><span class="n">strip</span><span class="p">()</span> <span class="k">for</span> <span class="n">att</span> <span class="ow">in</span> <span class="n">att_str</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s">&#39;,&#39;</span><span class="p">)]</span></div><div class='line' id='LC67'><br/></div><div class='line' id='LC68'><br/></div><div class='line' id='LC69'><span class="c"># Function for getting data out of SoundCloud object (null if missing)</span></div><div class='line' id='LC70'><br/></div><div class='line' id='LC71'><span class="k">def</span> <span class="nf">obj_atts_list</span><span class="p">(</span><span class="n">obj</span><span class="p">,</span> <span class="n">att_list</span><span class="p">):</span></div><div class='line' id='LC72'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">l</span> <span class="o">=</span> <span class="p">[]</span></div><div class='line' id='LC73'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="n">att</span> <span class="ow">in</span> <span class="n">att_list</span><span class="p">:</span></div><div class='line' id='LC74'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">try</span><span class="p">:</span></div><div class='line' id='LC75'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">l</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="nb">getattr</span><span class="p">(</span><span class="n">obj</span><span class="p">,</span><span class="n">att</span><span class="p">))</span></div><div class='line' id='LC76'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">except</span> <span class="ne">AttributeError</span><span class="p">:</span></div><div class='line' id='LC77'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">l</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="s">&#39;NULL&#39;</span><span class="p">)</span></div><div class='line' id='LC78'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">l</span></div><div class='line' id='LC79'><br/></div><div class='line' id='LC80'><br/></div><div class='line' id='LC81'><span class="c"># Generalised function for putting data into tables created</span></div><div class='line' id='LC82'><span class="c"># above, based on what&#39;s currently in getSoundCloudData.py</span></div><div class='line' id='LC83'><br/></div><div class='line' id='LC84'><span class="k">def</span> <span class="nf">insert_data_loop</span><span class="p">(</span><span class="n">cursor</span><span class="p">,</span> <span class="n">table</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="n">att_list</span><span class="p">):</span></div><div class='line' id='LC85'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sql</span><span class="o">=</span><span class="s">&#39;INSERT INTO {} VALUES({})&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">table</span><span class="p">,(</span><span class="s">&#39;?, &#39;</span><span class="o">*</span><span class="nb">len</span><span class="p">(</span><span class="n">att_list</span><span class="p">))[:</span><span class="o">-</span><span class="mi">2</span><span class="p">])</span></div><div class='line' id='LC86'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="n">datum</span> <span class="ow">in</span> <span class="n">data</span><span class="p">:</span></div><div class='line' id='LC87'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">try</span><span class="p">:</span></div><div class='line' id='LC88'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">vals</span><span class="o">=</span><span class="nb">tuple</span><span class="p">(</span><span class="n">obj_atts_list</span><span class="p">(</span><span class="n">datum</span><span class="p">,</span><span class="n">att_list</span><span class="p">))</span></div><div class='line' id='LC89'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cursor</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span><span class="n">sql</span><span class="p">,</span><span class="n">vals</span><span class="p">)</span></div><div class='line' id='LC90'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">except</span> <span class="ne">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span></div><div class='line' id='LC91'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">print</span><span class="p">(</span><span class="s">&#39;Error adding {} to &#39;</span></div><div class='line' id='LC92'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;{}: {} {}&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">datum</span><span class="o">.</span><span class="n">id</span><span class="p">,</span><span class="n">table</span><span class="p">,</span><span class="n">e</span><span class="o">.</span><span class="n">message</span><span class="p">,</span><span class="n">e</span><span class="o">.</span><span class="n">args</span><span class="p">))</span></div><div class='line' id='LC93'><br/></div><div class='line' id='LC94'><br/></div><div class='line' id='LC95'><span class="c"># (Probably) more efficient version of the above. We hopefully won&#39;t</span></div><div class='line' id='LC96'><span class="c"># need the exception handling once we&#39;ve got it working properly.</span></div><div class='line' id='LC97'><br/></div><div class='line' id='LC98'><span class="k">def</span> <span class="nf">insert_data</span><span class="p">(</span><span class="n">cursor</span><span class="p">,</span> <span class="n">table</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="n">att_list</span><span class="p">):</span></div><div class='line' id='LC99'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sql</span><span class="o">=</span><span class="s">&#39;INSERT INTO {} VALUES({})&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">table</span><span class="p">,(</span><span class="s">&#39;?, &#39;</span><span class="o">*</span><span class="nb">len</span><span class="p">(</span><span class="n">att_list</span><span class="p">))[:</span><span class="o">-</span><span class="mi">2</span><span class="p">])</span></div><div class='line' id='LC100'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">vals</span> <span class="o">=</span> <span class="p">[</span><span class="nb">tuple</span><span class="p">(</span><span class="n">obj_atts_list</span><span class="p">(</span><span class="n">d</span><span class="p">,</span><span class="n">att_list</span><span class="p">))</span> <span class="k">for</span> <span class="n">d</span> <span class="ow">in</span> <span class="n">data</span><span class="p">]</span></div><div class='line' id='LC101'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cursor</span><span class="o">.</span><span class="n">executemany</span><span class="p">(</span><span class="n">sql</span><span class="p">,</span><span class="n">vals</span><span class="p">)</span></div><div class='line' id='LC102'><br/></div><div class='line' id='LC103'><br/></div><div class='line' id='LC104'><span class="c"># Unit tests follow. N.B. if this module is imported by e.g.</span></div><div class='line' id='LC105'><span class="c"># getSoundCloudData.py, test1() and test2() provide a model for how</span></div><div class='line' id='LC106'><span class="c"># the above functions can be called.</span></div><div class='line' id='LC107'><br/></div><div class='line' id='LC108'><span class="k">class</span> <span class="nc">placeholder</span><span class="p">():</span></div><div class='line' id='LC109'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">pass</span></div><div class='line' id='LC110'><br/></div><div class='line' id='LC111'><br/></div><div class='line' id='LC112'><span class="k">def</span> <span class="nf">dummy_data</span><span class="p">():</span></div><div class='line' id='LC113'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ph1</span> <span class="o">=</span> <span class="n">placeholder</span><span class="p">()</span></div><div class='line' id='LC114'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ph1</span><span class="o">.</span><span class="n">id</span> <span class="o">=</span> <span class="mi">12345</span></div><div class='line' id='LC115'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ph2</span> <span class="o">=</span> <span class="n">placeholder</span><span class="p">()</span></div><div class='line' id='LC116'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ph2</span><span class="o">.</span><span class="n">id</span> <span class="o">=</span> <span class="mi">67890</span></div><div class='line' id='LC117'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ph2</span><span class="o">.</span><span class="n">user_id</span> <span class="o">=</span> <span class="mi">11102</span></div><div class='line' id='LC118'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="p">[</span><span class="n">ph1</span><span class="p">,</span><span class="n">ph2</span><span class="p">]</span></div><div class='line' id='LC119'><br/></div><div class='line' id='LC120'><br/></div><div class='line' id='LC121'><span class="k">def</span> <span class="nf">test1</span><span class="p">():</span></div><div class='line' id='LC122'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">test_data</span> <span class="o">=</span> <span class="n">dummy_data</span><span class="p">()</span></div><div class='line' id='LC123'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">connection</span> <span class="o">=</span> <span class="n">sqlite3</span><span class="o">.</span><span class="n">connect</span><span class="p">(</span><span class="s">&#39;test1.sqlite&#39;</span><span class="p">)</span></div><div class='line' id='LC124'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cursor</span> <span class="o">=</span> <span class="n">connection</span><span class="o">.</span><span class="n">cursor</span><span class="p">()</span></div><div class='line' id='LC125'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">create_table</span><span class="p">(</span><span class="n">cursor</span><span class="p">,</span><span class="s">&#39;dummy&#39;</span><span class="p">,</span><span class="n">dummy_table_creator</span><span class="p">)</span></div><div class='line' id='LC126'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">insert_data</span><span class="p">(</span><span class="n">cursor</span><span class="p">,</span><span class="s">&#39;dummy&#39;</span><span class="p">,</span><span class="n">test_data</span><span class="p">,</span></div><div class='line' id='LC127'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">att_list</span><span class="p">(</span><span class="n">att_string</span><span class="p">(</span><span class="n">dummy_table_creator</span><span class="p">)))</span></div><div class='line' id='LC128'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">connection</span><span class="o">.</span><span class="n">commit</span><span class="p">()</span></div><div class='line' id='LC129'><br/></div><div class='line' id='LC130'><br/></div><div class='line' id='LC131'><span class="k">def</span> <span class="nf">test2</span><span class="p">():</span></div><div class='line' id='LC132'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">test_data</span> <span class="o">=</span> <span class="n">dummy_data</span><span class="p">()</span></div><div class='line' id='LC133'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">connection</span> <span class="o">=</span> <span class="n">sqlite3</span><span class="o">.</span><span class="n">connect</span><span class="p">(</span><span class="s">&#39;test2.sqlite&#39;</span><span class="p">)</span></div><div class='line' id='LC134'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cursor</span> <span class="o">=</span> <span class="n">connection</span><span class="o">.</span><span class="n">cursor</span><span class="p">()</span></div><div class='line' id='LC135'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">create_table</span><span class="p">(</span><span class="n">cursor</span><span class="p">,</span><span class="s">&#39;tracks&#39;</span><span class="p">,</span><span class="n">tracks_table_creator</span><span class="p">)</span></div><div class='line' id='LC136'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">insert_data</span><span class="p">(</span><span class="n">cursor</span><span class="p">,</span><span class="s">&#39;tracks&#39;</span><span class="p">,</span><span class="n">test_data</span><span class="p">,</span></div><div class='line' id='LC137'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">att_list</span><span class="p">(</span><span class="n">att_string</span><span class="p">(</span><span class="n">tracks_table_creator</span><span class="p">)))</span></div><div class='line' id='LC138'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">connection</span><span class="o">.</span><span class="n">commit</span><span class="p">()</span></div></pre></div></td>
          </tr>
        </table>
  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" class="js-jump-to-line" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2014 <span title="0.02824s from github-fe123-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-fullscreen-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="js-fullscreen-contents" placeholder="" data-suggester="fullscreen_suggester"></textarea>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped tooltipped-w" aria-label="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped tooltipped-w"
      aria-label="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-remove-close close js-ajax-error-dismiss"></a>
      Something went wrong with that request. Please try again.
    </div>

  </body>
</html>

