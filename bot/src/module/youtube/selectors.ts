export class Common {
    static __URL__: string = "https://youtube.com";
    static __SEARCHINPUT__: string = "input#search";
    static __SEARCHBUTTON__: string = "button#search-icon-legacy";
    static __AGREEBUTTON__: string = "ytd-button-renderer.ytd-consent-bump-v2-lightbox:nth-child(2) > yt-button-shape:nth-child(1) > button:nth-child(1) > yt-touch-feedback-shape:nth-child(2) > div:nth-child(1) > div:nth-child(2)"; //button.VfPpkd-LgbsSe 
    static __AGREEBUTTON2__: string = "ytd-app > ytd-consent-bump-v2-lightbox > tp-yt-paper-dialog > div > div > div > div > ytd-button-renderer > a > tp-yt-paper-button > yt-formatted-string";
    static __NOSIGNBUTTON__: string = "#dismiss-button > yt-button-renderer > a"
    static __HOMEBUTTON__: string = "ytd-topbar-logo-renderer.style-scope:nth-child(4) > a:nth-child(1) > div:nth-child(1) > ytd-logo:nth-child(1) > yt-icon:nth-child(1) > yt-icon-shape:nth-child(1) > icon-shape:nth-child(1) > div:nth-child(1)";//"a.ytd-topbar-logo-renderer";
    static __URL_WATCH__: string = "https://www.youtube.com/watch?v=";
}

export class Homepage {
    static __PROPOSALS__: string = "#meta";
    static __ELEMENT__URL: string = "a";
    static __ELEMENT__TITLE: string = "h3";
    static __ELEMENT__CHANNEL: string = "#text";
}

export class VideoPage {
    static __CATEGORY__: string = "meta[itemprop='genre']";
    static __VIEWS__: string = ".view-count";
    static __REGIONALLOWED__: string = "meta[itemprop='regionAllowed']";
    static __UNLISTED__: string = "meta[itemprop='unlisted']";
    static __PAID__: string = "meta[itemprop='paid']";
    static __DESCRIPTION__: string = "#description > .content";
    static __ISFAMILYFRIENDLY__: string = "meta[itemprop='isFamilyFriendly']";
    static __SUBSCRIBERS__: string = "#owner-sub-count";//"#owner-sub-count";
    static __DURATION__: string = "meta[itemprop='duration']";
    static __DATE__: string = "#date > yt-formatted-string";//"#date > yt-formatted-string";
    static __COMMENT__: string = "#count > yt-formatted-string > span:nth-child(1)";
    static __DISLIKE__: string = "ytd-toggle-button-renderer.style-scope:nth-child(2) > a > yt-formatted-string";
    static __LIKE__: string = "ytd-menu-renderer.ytd-watch-metadata > div:nth-child(1) > segmented-like-dislike-button-view-model:nth-child(1) > yt-smartimation:nth-child(1) > div:nth-child(1) > div:nth-child(1) > like-button-view-model:nth-child(1) > toggle-button-view-model:nth-child(1) > button-view-model:nth-child(1) > button:nth-child(1) > div:nth-child(2)";
    static __TAGS__: string = "ytd-video-primary-info-renderer yt-formatted-string a";
    static __AUTHOR__: string = "ytd-channel-name.ytd-video-owner-renderer > div:nth-child(1) > div:nth-child(1) > yt-formatted-string:nth-child(1) > a:nth-child(1)";
    static __TITLE__: string = "yt-formatted-string.ytd-video-primary-info-renderer:nth-child(1)";
    static __AUTOPLAY__: string = "#dismissible > div.details";
    static __AUTOPLAY__TITLE: string = "#video-title.style-scope.ytd-compact-video-renderer";
    static __AUTOPLAY__URL: string = "#dismissible > div > div.metadata.style-scope.ytd-compact-video-renderer > a";
    static __PROPOSALS__: string = "ytd-compact-video-renderer.style-scope"
}

export class SearchPage {
    static __RESULTELEMENT__ = "yt-formatted-string";
    static __TITLE__: string = "ytd-video-renderer.style-scope > div > div > div > div > h3 > a";
    static __CHANNELFILTER__: string = "#filter-menu > #container > ytd-toggle-button-renderer > a";
    static __CHANNELFILTERBUTTON__: string = "ytd-search-filter-group-renderer.style-scope:nth-child(2) > ytd-search-filter-renderer:nth-child(4) > a:nth-child(1)";
    static __RESULTELEMENT1__: string = ""
    static __RESULTELEMENT2__: string = ""
}

export class ChannelPage {
    static __VIDEOSBUTTON__: string = "tp-yt-paper-tab.style-scope:nth-child(4)";
    static __CHANNELNAME__: string = "#meta > #channel-name > #container > #text-container > #text";
    static __METACHANNELNAME__: string = "#header #inner-header-container #title"
}
