import {Action} from "../../abstract/action";
import {Video} from './video';
import {VideoScrapper} from './videoScrapper';
import {Common, VideoPage, SearchPage, ChannelPage, Homepage} from './selectors';

export class YoutubeAction extends Action {

    constructor(page: any, args: any) {
        super(page, args)

        this.scrapper = new VideoScrapper();
    }

    /*
    ####################### Cookies And Sign Section ##############################
    */

    async postConf() {
        try {
            await this.page.goto(Common.__URL__, {waitUntil: 'networkidle2', timeout: 0});
        } catch (error) {
            try {
                await this.page.goto(Common.__URL__, {waitUntil: 'networkidle2', timeout: 0});
            } catch (error) {
                console.log("STRONG ERROR CONNEXION FAILED");
                console.log(error);
                process.exit()
            }
        }

        await this.preCondition()
        await this.noSign()
    }

    async preCondition() {
        let agree = null
        //console.log("agree = null");

        try {
            await this.page.waitForSelector(Common.__AGREEBUTTON__);
        }
        catch(error) {
            try {
            await this.page.goto(Common.__URL__, {waitUntil: 'networkidle2', timeout: 0});
            } 
            catch (error) {
                console.log("ERROR CONNEXION FAILED (second)");
                console.log(error);
                process.exit()
            }
        }

        try {
            await this.page.waitForSelector(Common.__AGREEBUTTON__);
            agree = await this.scrapper.getElement(this.page, Common.__AGREEBUTTON__)
        } catch (error) {
            console.log("Page could not be loaded.");
            let path = Date.now() + '_error.png';
            await this.page.screenshot({path: path, fullPage: true});
            try {
                await this.page.waitFor(Common.__AGREEBUTTON2__);
                const buttons = await this.page.$$(Common.__AGREEBUTTON2__);
                agree = buttons[2]
            } catch (error) {
                console.log("FAILED TWICE !!");
                try {
                    await this.isFullyLoad()
                } catch (error) {
                    console.log("KILL !!");
                    process.exit()
                }
            }

        }
        if (agree !== null) {
            await this.lauchCmd(agree, 'click', '')
        }
        //console.log("got out...");
    }

    async noSign() {
        await this.page.waitFor(2000);
        const agree = await this.scrapper.getElement(this.page, Common.__NOSIGNBUTTON__)
        if (agree !== null) {
            await this.lauchCmd(agree, 'click', '')
            await this.page.waitFor(2000);
        }
    }

    /*
    ####################### End Cookies And Sign Section ##############################
    */

    /*
    ####################### Scroll Section ##############################
    */

    async scrollUntil(max_selection: number) {
        let videos = [];
        let start = 0;
        let end = 500;
        while (videos.length < max_selection + 10) {
            await this.page.evaluate('window.scrollTo(' + start + ', ' + end + ')')
            videos = await this.scrapper.getHomeProposals(this.page);
            await this.page.waitFor(1000)
            start = end;
            end = end + 500;
        }
    }

    async scrollUntilId() {
        let start = 0;
        let end = 500;
        let previousWinHeight = -1
        let winHeight = (+await this.page.evaluate('document.body.getBoundingClientRect().top')) * -1
        while (winHeight > previousWinHeight) {
            const videos = await this.scrapper.getHomeProposals(this.page);
            if (typeof this.video_id !== 'undefined') {
                for (let i = 0; i < videos.length; i++) {
                    const url = await this.scrapper.getHomeUrls(videos[i])
                    if (url.includes(this.video_id)) {
                        return
                    }
                }
            }
            await this.page.evaluate('window.scrollTo(' + start + ', ' + end + ')')
            await this.page.waitFor(1000)
            previousWinHeight = winHeight
            winHeight = (+await this.page.evaluate('document.body.getBoundingClientRect().top')) * -1
            start = end;
            end = end + 500;
        }
        return
    }

    async scrollToEnd() {
        let videos = [];
        let start = 0;
        let end = 500;
        let previousWinHeight = -1
        let winHeight = (+await this.page.evaluate('document.body.getBoundingClientRect().top')) * -1
        while (winHeight > previousWinHeight) {
            await this.page.evaluate('window.scrollTo(' + start + ', ' + end + ')')
            videos = await this.scrapper.getHomeProposals(this.page);
            let path = Date.now() + '_error.png';
            await this.page.screenshot({path: path, fullPage: true});
            //console.log("okokokok");
            //console.log(videos.length - 1);
            await this.page.waitFor(1000)
            previousWinHeight = winHeight
            winHeight = (+await this.page.evaluate('document.body.getBoundingClientRect().top')) * -1
            start = end;
            end = end + 500;
        }
        //console.log(videos.length - 1);
        return videos.length - 1
    }

    async scrollUntilChannelId() {
        let start = 0;
        let end = 500;
        let previousWinHeight = -1
        let winHeight = (+await this.page.evaluate('document.body.getBoundingClientRect().top')) * -1
        while (winHeight > previousWinHeight) {
            const videos = await this.scrapper.getChannelFilter(this.page);
            if (typeof this.channel_id !== 'undefined') {
                for (let i = 0; i < videos.length; i++) {
                    const url = await this.scrapper.getHomeUrls(videos[i])
                    if (url.includes(this.channel_id)) {
                        return
                    }
                }
            }
            await this.page.evaluate('window.scrollTo(' + start + ', ' + end + ')')
            await this.page.waitFor(1000)
            previousWinHeight = winHeight
            winHeight = (+await this.page.evaluate('document.body.getBoundingClientRect().top')) * -1
            start = end;
            end = end + 500;
        }
        return
    }

    /*
    ####################### End Scroll Section ##############################
    */

    /*
    ####################### Click Section ##############################
    */

    async clickHome() {
        await this.page.waitFor(Common.__HOMEBUTTON__);
        const homebutton = await this.scrapper.getElement(this.page, Common.__HOMEBUTTON__)
        await this.lauchCmd(homebutton, "click", '')
        await this.page.waitFor(Common.__HOMEBUTTON__)
        await this.page.reload({waitUntil: ["networkidle0", "domcontentloaded"]});
    }

    async clickOnChannelFilter() {
        // await this.isFullyLoad()
        try {
            let path = Date.now() + '_error.png';
            await this.page.screenshot({path: path, fullPage: true});
            await this.page.waitFor(3000);
            await this.page.waitFor(SearchPage.__CHANNELFILTER__);
        } catch (e) {
            // if stuck on search button click, rerun the sequence
            console.log("stuck on search");
            await this.page.waitFor(3000);
            await this.enterSearchInput();
            await this.page.waitFor(3000);
            await this.page.waitFor(SearchPage.__CHANNELFILTER__);
        }
        
        const filter = await this.scrapper.getElement(this.page, SearchPage.__CHANNELFILTER__)
        if (filter !== null) {
            await this.lauchCmd(filter, 'click', '')
            await this.page.waitFor(SearchPage.__CHANNELFILTERBUTTON__);
            const channel_filter = await this.scrapper.getElement(this.page, SearchPage.__CHANNELFILTERBUTTON__)
            await this.lauchCmd(channel_filter, 'click', '')
        }
        else {
            console.log("big big error");
        }
    }

    async getVideoDetails() {
        const alea = this.getAlea()
        await this.page.waitFor(VideoPage.__TITLE__);
        await this.page.waitFor(alea);
        const video = new Video(await this.page.url(), this.videoViewsNB);
        await this.scrapper.fill(video, this.page)
        video.setType("regular")
        video.setWatchTime(alea)
        video.setActionNB(this.actionNB)
        video.addVideoViews()
        this.videoViewsNB = this.videoViewsNB + 1
        console.log(JSON.stringify(video) + ',');
        await this.getProposals(video.getUrl())
    }

    async clickOn(element: any) {
        await this.lauchCmd(element, "click", '')
        await this.getVideoDetails()
    }

    async getProposals(id: string) {
        const proposals = await this.scrapper.getProposals(this.page)
        for (let i = 0; i < proposals.length; i++) {
            const video = new Video(await this.scrapper.getHomeUrls(proposals[i]), this.videoViewsNB);
            video.setAuthor(await this.scrapper.getProposalAuthor(proposals[i]));
            video.setTitle(await this.scrapper.getHomeTitles(proposals[i]));
            video.setViews(await this.scrapper.getHomeViews(proposals[i]))
            video.setDuration(await this.scrapper.getHomeDuration(proposals[i]))
            video.setDate(await this.scrapper.getHomeDate(proposals[i]))
            video.setActionNB(this.actionNB)
            video.setParentId(id)
            video.setType("proposal")
            if (video['url'] === "") {
                continue
            }
            console.log(JSON.stringify(video) + ',');
        }
    }

    /*
    ####################### End Click Section ##############################
    */

    /*
    ####################### Search Section ##############################
    */

    async searchChannel(): Promise<any> {
        // await this.isFullyLoad()
        try {
            await this.page.waitFor(Common.__SEARCHINPUT__);
        } catch (error) {
            console.log("error on  catching search input in channelSniffer");
            return null;
        }
        await this.page.waitFor(3000)
        //console.log("could wait for 3000");
        await this.enterSearchInput()
        await this.page.waitFor(3000)
        console.log("could wait for 3000");
        await this.clickOnChannelFilter()
        await this.scrollUntilChannelId()


        let path = Date.now() + '_error.png';
        await this.page.screenshot({path: path, fullPage: true});
        const videos = await this.scrapper.getChannelFilter(this.page);
        let searchSelection = 0;
        if (typeof this.channel_id !== 'undefined') {
            console.log("defined");
            for (let i = 0; i < videos.length; i++) {
                const url = await this.scrapper.getHomeUrls(videos[i])
                if (url.includes(this.channel_id)) {
                    console.log("found channel !");
                    searchSelection = i;
                    break;
                }
            }
        }

        let selections = await this.page.$$(Homepage.__PROPOSALS__);
        let selection = videos[searchSelection]
        if (!selection) {
            selection = await this.page.$('#items > ytd-video-renderer:nth-child(' + searchSelection + ')');
        }
        await this.lauchCmd(selection, "click", '')
        if (!this.customYtChannel && !this.metaChannel) {
            // For channels like national news or any kind of youtube compilation channels we do not need this action
            await this.page.waitFor(ChannelPage.__VIDEOSBUTTON__);
            const videos_button = await this.scrapper.getElement(this.page, ChannelPage.__VIDEOSBUTTON__)
            if (videos_button !== null) {
                await this.lauchCmd(videos_button, 'click', '')
            }
        }

        await this.page.waitFor(3000)
        await this.scrollToEnd()
        const url = await this.page.url();
        await this.page.goto(url)
        let full_channel_videos = []
        let channelNameSelector;
        if (this.metaChannel) {
            channelNameSelector = ChannelPage.__METACHANNELNAME__;
        } else {
            channelNameSelector = ChannelPage.__CHANNELNAME__;
        }

        await this.page.waitFor(channelNameSelector);
        const channel_name_element = await this.scrapper.getElement(this.page, channelNameSelector)
        const channel_name = await this.page.evaluate((el: any) => el.innerText, channel_name_element);
        //path = Date.now() + '_error.png';
        //await this.page.screenshot({path: path, fullPage: true});

        const videos_channel = await this.scrapper.getHomeProposals(this.page);
        for (let i = 0; i < videos_channel.length; i++) {
            const video = new Video(await this.scrapper.getHomeUrls(videos_channel[i]), this.videoViewsNB);
            video.setAuthor(channel_name);
            video.setTitle(await this.scrapper.getHomeTitles(videos_channel[i]));
            video.setViews(await this.scrapper.getHomeViews(videos_channel[i]))
            video.setDuration(await this.scrapper.getHomeDuration(videos_channel[i]))
            video.setDate(await this.scrapper.getHomeDate(videos_channel[i]))
            video.setDuration(await this.scrapper.getHomeDuration(videos_channel[i]))
            video.setActionNB(this.actionNB)
            video.setType("ChannelSniffer")
            if (video['url'] === "") {
                continue
            }
            full_channel_videos.push(video)
        }
        return full_channel_videos
    }


    async search(): Promise<any> {
        // await this.page.waitFor(2000);
        // await this.isFullyLoad()
        try {
            await this.page.waitFor(Common.__SEARCHINPUT__);
        } catch (error) {
            return null;
        }
        await this.enterSearchInput();
        await this.page.waitFor(Homepage.__PROPOSALS__);
        await this.scrollUntilId()
        let path = Date.now() + '_thing.png';
        await this.page.screenshot({path: path, fullPage: true});
        const videos = await this.scrapper.getHomeProposals(this.page);
        let searchSelection = null;
        if (typeof this.video_id !== 'undefined') {
            for (let i = 0; i < videos.length; i++) {
                const url = await this.scrapper.getHomeUrls(videos[i])
                if (url.includes(this.video_id)) {
                    searchSelection = i;
                    break;
                }
            }
        }
        if (searchSelection === null) { // means searched video id didn't appear inside search results
            await this.page.goto(Common.__URL_WATCH__ + this.video_id);
            await this.getVideoDetails();
        } else {
            let selections = await this.page.$$(Homepage.__PROPOSALS__);
            let selection = selections[searchSelection]
            if (!selection) {
                selection = await this.page.$('#items > ytd-video-renderer:nth-child(' + searchSelection + ')');
            }
            await this.clickOn(selection)
        }
    }

    private async enterSearchInput() {
        await this.page.click(Common.__SEARCHINPUT__); // to mimic human behavior click the search input and wait a bit ...
        await this.page.waitFor(500); // ... this allows bypassing bot checks in some cases
        await this.page.$eval(Common.__SEARCHINPUT__, (el: any, term: string) => el.value = term, this.searchTerm);
        await this.page.waitFor(Common.__SEARCHBUTTON__);
        let current_url = await this.page.url();
        await this.page.click(Common.__SEARCHBUTTON__);
        let next_url = await this.page.url();
        if (next_url === current_url) {//url should be changed after search button click...
            await this.page.waitFor(500);
            await this.page.click(Common.__SEARCHBUTTON__); //... if not try clicking again
            let next_url = await this.page.url();
            if (next_url === current_url) {// one last time
                await this.page.waitFor(500);
                await this.page.click(Common.__SEARCHBUTTON__);
                let next_url = await this.page.url();
                if (next_url === current_url) {
                    console.log("could not load the expected new page");
                    //better than fetching wrong data from homepage instead of search results
                    process.exit(); // close the app
                }
            }
        }
    }

    /*
      ####################### End Search Section ##############################
      */

    getRandomArbitrary(min: number, max: number) {
        return Math.random() * (max - min) + min;
    }

    getAlea() {
        return this.getRandomArbitrary(this.watchTime - this.alea, this.watchTime + this.alea)
    }

    async getFullHomepage() {
        // await this.isFullyLoad()
        try {
            await this.page.waitForFunction('document.querySelectorAll("ytd-thumbnail > a").length >=' + 10);
        } catch (error) {

        }

        const max_selection = await this.scrollToEnd();
        const proposals = await this.scrapper.getHomeProposals(this.page);
        //let path = Date.now() + '_error.png';
        //await this.page.screenshot({path: path, fullPage: true});
        //console.log("je test un truc");
        //console.log(proposals);
        for (let i = 0; i < max_selection; i++) {
            //console.log("je test un truc 100");
            const video = new Video(await this.scrapper.getHomeUrls(proposals[i]), this.videoViewsNB);
            video.setHomePosition(i);
            video.setAuthor(await this.scrapper.getHomeChanels(proposals[i]));
            video.setTitle(await this.scrapper.getHomeTitles(proposals[i]));
            video.setDuration(await this.scrapper.getHomeDuration(proposals[i]));
            video.setViews(await this.scrapper.getHomeViews(proposals[i]))
            video.setDate(await this.scrapper.getHomeDate(proposals[i]))
            video.setRefreshNB(this.refreshNB)
            video.setType("homepage")
            // await saveVideo(video,this.id)
            video.setActionNB(this.actionNB)
            console.log(JSON.stringify(video) + ',');
        }
        // this.refreshNB++
    }

    getRandomInt(max: number) {
        return Math.floor(Math.random() * Math.floor(max));
    }

    async getRandomHomeElement() {
        let selection = await this.scrapper.getHomeProposals(this.page)
        let rand = +this.getRandomInt(selection.length)
        return selection[rand]
    }

    async getAutoplay() {
        // await this.isFullyLoad()
        await this.page.waitFor(VideoPage.__AUTOPLAY__)
        let selection = await this.page.$$(VideoPage.__AUTOPLAY__);
        return selection[0]
    }

    async fillAutoplaysearch() {
        try {
            this.searchTerm = await this.page.$eval(VideoPage.__AUTOPLAY__TITLE, (el: any) => el.textContent.trim())
            this.video_id = await this.page.$eval(VideoPage.__AUTOPLAY__URL, (el: any) => el.href.substring(el.href.lastIndexOf('v=') + 2, el.href.length))
            let i = 0;
            while(this.video_id.includes("/shorts/")) {
                const proposals = await this.scrapper.getProposals(this.page)
                const video = new Video(await this.scrapper.getHomeUrls(proposals[i]), this.videoViewsNB);
                this.searchTerm = (await this.scrapper.getHomeTitles(proposals[i])).trim()//await this.page.$eval(VideoPage.__AUTOPLAY__TITLE, (el: any) => el.textContent.trim())
                this.video_id = video.getUrl();
            }
        } catch (error) {
            this.video_id = await this.page.$eval(VideoPage.__AUTOPLAY__URL)
            if(this.video_id)
            console.log("common error")
            let path = Date.now() + '_error.png';
            await this.page.screenshot({path: path, fullPage: true});
            process.exit()
        }
    }

    async isFullyLoad() {
        await this.page.waitForFunction('document.querySelectorAll("ytd-guide-renderer > #sections > ytd-guide-section-renderer > #items > ytd-guide-entry-renderer > a").length > 10');
    }

}
