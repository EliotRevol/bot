import {ArgumentParser} from "argparse";
import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import {Job} from "./jobs/job";
import {Fetch} from "./jobs/fetch";
import {WatchOne} from "./jobs/watchOne";
import {Autoplay} from './jobs/autoplay';
import {ChannelSniffer} from './jobs/channelSniffer';
import {FetchAutoplay} from './jobs/fetchAutoplay';
import {YoutubeAction} from './module/youtube/youtubeAction'
import fs from 'fs';

class Crawler {

    async initBrowser() {
        await puppeteer.use(StealthPlugin());
        let browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--enable-file-cookies']
        });
        return browser;
    }

    async initPage(browser: any, cookies: any) {
        const page = await browser.newPage()
        // console.log("lenght "+cookies['cookies'].length);

        if (Object.keys(cookies).length > 0) {
            // console.log("set cookies");
            await page.setCookie(...cookies['cookies']);
        }
        await page.setDefaultNavigationTimeout(0);
        await page.setRequestInterception(true);
        page.on('request', (request: any) => {
            if (request.resourceType() === 'media')
                request.abort();
            else
                request.continue();
        });
        await page.setViewport({width: 1535, height: 756})
        if (args['height'] && args['width']) {
            await page.setViewport({width: +args['width'], height: +args['height']})
        }
        if (args['userAgent']) {
            await page.setUserAgent(args['userAgent']);
        }
        if (args['lang']) {
            await page.setExtraHTTPHeaders({
                'Accept-Language': args['lang']
            });
        }
        return page;
    }

    async readCookies(filename: string) {
        let cookies = {}
        if (fs.existsSync('input/' + filename + '.json')) {
            let rawdata = fs.readFileSync('input/' + filename + '.json');
            cookies = JSON.parse(rawdata.toString());
        }
        // console.log(cookies);
        return cookies
    }

    async writeCookies(page: any, filename: string) {
        const cookies = await page._client.send('Network.getAllCookies')
        let data = JSON.stringify(cookies);
        fs.writeFileSync('input/' + filename + '.json', data);
    }

    async eventExecutor(page: any, events: Array<string>) {
        let job: Job
        let action = new YoutubeAction(page, [])
        await action.postConf()
        let refreshNB = 0
        let videoViewsNB = 0
        let actionNB = -1
        //console.log("on est dans l'event executor");
        for (const index in events) {
            //console.log("index is "+index);
            if (events.hasOwnProperty(index)) {
                const element = events[index];
                let event = JSON.parse(element);
                event['actionNB'] = actionNB
                switch (event['type']) {

                    case 'watchOne':
                        //console.log("watch one ");
                        job = new WatchOne(page, event, refreshNB, videoViewsNB)
                        videoViewsNB = videoViewsNB + 1
                        break;

                    case 'fetch':
                        //console.log("fetch ");
                        job = new Fetch(page, event, refreshNB, videoViewsNB)
                        break;

                    case 'autoplay':
                        //console.log("autoplay ");
                        job = new Autoplay(page, event, refreshNB, videoViewsNB)
                        videoViewsNB = videoViewsNB + event['searchSelection']
                        break;

                    case 'fetchAutoplay':
                        //console.log("fetch auto play ");
                        job = new FetchAutoplay(page, event, refreshNB, videoViewsNB)
                        videoViewsNB = videoViewsNB + event['searchSelection'] - 1
                        break;

                    case 'channelSniffer':
                        job = new ChannelSniffer(page, event, refreshNB, videoViewsNB)
                        videoViewsNB = videoViewsNB + event['searchSelection']
                        break;

                    default:
                        //console.log("running default");
                        job = new Fetch(page, event, refreshNB, videoViewsNB)
                        break;
                }
                await job.execute();
                actionNB = job.action.actionNB;
                refreshNB = job.action.refreshNB;
            }
        }
    }

    async crawl(args: any) {
        //console.log("sous crawler");
        let browser = await this.initBrowser();
        let cookies = {}
        //console.log("browser inited");
        if ('cookies' in args) {
            cookies = await this.readCookies(args['cookies'])
        }

        //console.log("page inited");
        let page = await this.initPage(browser, cookies);
        try {
            await this.eventExecutor(page, args['events'])
        } catch (e) {
            // in case of any exception, bot will log to stderr and shut down without any output
            console.error(e);
			console.error("Error, saving screenshot");
            let path = Date.now() + '_error.png';
            await page.screenshot({path: path, fullPage: true});
            console.error("saved screenshot to " + path)
        }
        if ('cookies' in args && typeof args['cookies'] !== 'undefined') {
            await this.writeCookies(page, args['cookies'])
        }
        await browser.close();
    }
}

const crawler = new Crawler();
const parser = new ArgumentParser({
    description: 'Argparse example'
});

// parser.add_argument('-v', '--version', { action: 'version', version });
// parser.add_argument('type', { help: 'homepage | watchOne | followAutoplay' });
parser.add_argument('-s', '--searchTerm', {help: 'searchTerm'});
parser.add_argument('-i', '--video_id', {help: 'Video Id'});
parser.add_argument('-ci', '--channel_id', {help: 'Channel Id'});
parser.add_argument('-w', '--watchTime', {help: 'watchTime'});
parser.add_argument('-ss', '--searchSelection', {help: 'searchSelection'});
parser.add_argument('-c', '--cookies', {help: 'cookies filename'});
parser.add_argument('-e', '--events', {nargs: '+'});
parser.add_argument('-u', '--userAgent', {help: 'User agent'});
parser.add_argument('-wr', '--width', {help: 'Resolution width'});
parser.add_argument('-hr', '--height', {help: 'Resolution height'});
parser.add_argument('-l', '--lang', {help: 'Browser Language'});
parser.add_argument("--save_html", {help: 'Save visited HTMLs flag', action: 'store_true'})

const args = parser.parse_args()
export {args};
//console.log("on est sous test là");
crawler.crawl(args);

