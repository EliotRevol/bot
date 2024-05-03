import {Scrapper} from "./../../abstract/scrapper";
import {Video} from './video'
import {Homepage, SearchPage, VideoPage} from './selectors'
import {args} from './../../main'

export class VideoScrapper extends Scrapper {

    async getChannelFilter(page: any): Promise<any> {
        try {
            return await page.$$("ytd-channel-renderer.style-scope > div:nth-child(2) > div:nth-child(2)");
        } catch (error) {
            return null;
        }
    }

    async getChannelTitle(page: any): Promise<string> {
        try {
            return (await page.$eval("#channel-name > #container > #text-container > #text", (a: any) => a.textContent)).replace(/['"]+/g, '');
        } catch (error) {
            return null;
        }
    }

    async getHomeProposals(page: any): Promise<any> {
        try {
            return await page.$$(Homepage.__PROPOSALS__);
        } catch (error) {
            return null;
        }
    }

    async getHomeChanels(elementHandle: any): Promise<string> {
        try {
            return await elementHandle.$eval(Homepage.__ELEMENT__CHANNEL, (a: any) => a.textContent);
        } catch (error) {
            return "bigtest";
        }
    }

    async getHomeViews(elementHandle: any): Promise<string> {
        try {
            return await elementHandle.$eval("span.ytd-video-meta-block:nth-child(1)", (a: any) => a.textContent);
        } catch (error) {
            try {
                return await elementHandle.$eval("span:nth-child(1)", (a: any) => a.textContent);
            } catch (e) {
                return "bigtest"
            }
        }
    }

    async getHomeDate(elementHandle: any): Promise<string> {
        try {
            return await elementHandle.$eval("span.ytd-video-meta-block:nth-child(2)", (a: any) => a.textContent);
        } catch (error) {
            try {
                return await elementHandle.$eval("span:nth-child(2)", (a: any) => a.textContent);
            } catch (e) {
                return "bigtest"
            }
        }
    }

    async getHomeDuration(elementHandle: any): Promise<string> {
        try {
            const parent = await elementHandle.getProperty("parentNode")
            const grandParent = await parent.getProperty("parentNode")
            return (await grandParent.$eval("span", (a: any) => a.textContent)).replace(/\s|\n/g, '');
        } catch (error) {
            return "bigtest";
        }
    }


    async getHomeTitles(elementHandle: any): Promise<string> {
        try {
            return (await elementHandle.$eval(Homepage.__ELEMENT__TITLE, (a: any) => a.textContent)).replace(/['"]+/g, '');
        } catch (error) {
            return "bigtest";
        }
    }

    async getHomeUrls(elementHandle: any): Promise<string> {
        try {
            return await elementHandle.$eval(Homepage.__ELEMENT__URL, (a: any) => a.href);
        } catch (error) {
            return "bigtest";
        }
    }

    async getResultElement(page: any) {
        try {
            return await page.$$(SearchPage.__RESULTELEMENT__);
        } catch (error) {
            return null;
        }
    }

    async getSearchTitle(page: any): Promise<string[]> {
        try {
            return await page.$$eval(SearchPage.__TITLE__, (anchors: any) => [].map.call(anchors, (a: any) => a.getAttribute('title')));
        } catch (error) {
            return [];
        }
    }

    async fill(video: Video, page: any) {

        const title = await this.getTitle(page);
        const views = await this.getViews(page);
        const author = await this.getAuthor(page);
        const tags = await this.getTags(page);
        const category = await this.getCategory(page);
        const date = await this.getDate(page);
        const duration = await this.getDuration(page);
        const subscribers = await this.getSubscribers(page);
        const isFamilyFriendly = await this.getIsFamilyFriendly(page);
        const description = await this.getDescription(page);
        const paid = await this.getPaid(page);
        const unlisted = await this.getUnlisted(page);
        const regionAllowed = await this.getRegionAllowed(page);
        const bodyHtml = await this.getFullHtml(page);
        const like = await this.getLike(page);
        const dislike = await this.getDislike(page);
        const comment = await this.getComment(page);

        video.setTitle(title);
        video.setViews(views);
        video.setAuthor(author);
        video.setTags(tags);
        video.setCategory(category);
        video.setDate(date);
        video.setDuration(duration);
        video.setSubscibers(subscribers);
        video.setIsFamilyFriendly(isFamilyFriendly);
        video.setDescription(description);
        video.setPaid(paid);
        video.setUnlisted(unlisted);
        video.setRegionAllowed(regionAllowed);
        if (args.save_html && video.getUrl().includes("youtube.com/watch?")) {
            video.setBodyHtml(bodyHtml); // save if only visited page is video
        }
        video.setLike(like);
        video.setDislike(dislike);
        video.setComment(comment);

    }

    async getProposals(page: any): Promise<any> {
        try {
            return page.$$(VideoPage.__PROPOSALS__)
        } catch (error) {
            return null
        }
    }

    async getProposalTitle(elementHandle: any): Promise<string> {
        try {
            return await elementHandle.$eval("#video-title", (a: any) => a.href);
        } catch (error) {
            return null
        }
    }

    async getProposalAuthor(elementHandle: any): Promise<string> {
        try {
            return (await elementHandle.$eval("ytd-channel-name > div > div > yt-formatted-string", (a: any) => a.textContent)).replace(/['"]+/g, '');
        } catch (error) {
            return null
        }
    }

    async getTitle(page: any): Promise<string> {
        try {
            return (await page.$eval(VideoPage.__TITLE__, (el: any) => el.textContent)).replace(/['"]+/g, '');
        } catch (error) {
            return null;
        }
    }

    async getAuthor(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__AUTHOR__, (el: any) => el.textContent);
        } catch (error) {
            return null;
        }
    }

    async getTags(page: any): Promise<string[]> {
        try {
            return await page.$$eval(VideoPage.__TAGS__, (anchors: any) => [].map.call(anchors, (tag: any) => tag.textContent));
        } catch (error) {
            console.log(error);
            return [];
        }
    }


    async getLike(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__LIKE__, (el: any) => el.textContent);
        } catch (error) {
            return null;
        }
    }

    async getDislike(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__DISLIKE__, (el: any) => el.textContent);
        } catch (error) {
            return null;
        }
    }

    async getComment(page: any): Promise<string> {
        try {
            await page.evaluate('window.scrollTo(0,500)')
            await page.waitFor(VideoPage.__COMMENT__)
            return await page.$eval(VideoPage.__COMMENT__, (el: any) => el.textContent);
        } catch (error) {
            return null;
        }
    }

    async getDate(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__DATE__, (el: any) => el.textContent);
        } catch (error) {
            return null;
        }
    }

    async getDuration(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__DURATION__, (el: any) => el.content);
        } catch (error) {
            return null;
        }
    }

    async getSubscribers(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__SUBSCRIBERS__, (el: any) => el.textContent);
        } catch (error) {
            return null;
        }
    }

    async getIsFamilyFriendly(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__ISFAMILYFRIENDLY__, (el: any) => el.content);
        } catch (error) {
            return null;
        }
    }

    async getDescription(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__DESCRIPTION__, (el: any) => el.textContent);
        } catch (error) {
            return null;
        }
    }

    async getPaid(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__PAID__, (el: any) => el.content);
        } catch (error) {
            return null;
        }
    }

    async getUnlisted(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__UNLISTED__, (el: any) => el.content);
        } catch (error) {
            return "False";
        }
    }

    async getRegionAllowed(page: any): Promise<string[]> {
        try {
            return await page.$$eval(VideoPage.__REGIONALLOWED__, (anchors: any) => [].map.call(anchors, (reg: any) => reg.textContent));
        } catch (error) {
            return null;
        }
    }

    async getCategory(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__CATEGORY__, (el: any) => el.content);
        } catch (error) {
            return null;
        }
    }

    async getViews(page: any): Promise<string> {
        try {
            return await page.$eval(VideoPage.__VIEWS__, (el: any) => el.textContent);
        } catch (error) {
            return null;
        }
    }

}
