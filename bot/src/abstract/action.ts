import {Scrapper} from './scrapper';

export class Action {
    protected max_depth: number
    protected max_selection: number
    protected cookies: string
    protected randomStep: boolean
    protected nbRandomStep: number
    protected step: number
    protected type: string
    protected current_depth: number
    protected current_selection: number
    public refreshNB: number = 0
    public searchTerm: string
    public searchSelection: number = 3
    protected watchTime: number = 60000
    protected page: any
    public video_id: string
    protected channel_id: string
    protected scrapper: Scrapper
    public id: number
    public getAll: boolean
    protected alea: number = 0
    public actionNB: number
    public videoViewsNB: number
    public customYtChannel: boolean
    public metaChannel: boolean;

    constructor(page: any, args: any) {
        this.page = page;
        if ('searchSelection' in args) {
            this.searchSelection = +args['searchSelection'];
        }
        if ('searchTerm' in args) {
            this.searchTerm = args['searchTerm'];
        }
        if ('video_id' in args) {
            this.video_id = args['video_id'];
        }
        if ('channel_id' in args) {
            this.channel_id = args['channel_id'];
        }
        if ('watchTime' in args) {
            this.watchTime = +args['watchTime'];
        }
        if ('getAll' in args) {
            this.getAll = args['getAll'];
        }
        if ('alea' in args) {
            this.alea = +args['alea'];
        }
        if ('actionNB' in args) {
            this.actionNB = +args['actionNB'];
        }
        if ('videoViewsNB' in args) {
            this.videoViewsNB = +args['videoViewsNB'];
        }
        if ('customYtChannel' in args) {
            this.customYtChannel = args['customYtChannel'];
        }
        if ('metaChannel' in args) {
            this.metaChannel = args['metaChannel']
        }
    }

    async lauchCmd(element: any, f: string, args: string) {
        try {
            await eval('element.' + f + '(' + args + ')')
        } catch (error) {
            const url = this.page.url();
            await this.page.goto(url)
            await this.page.waitFor(5000)
            try {
                await eval('element.' + f + '(' + args + ')')
            } catch (error) {
                try {
                    element = await this.page.$("#meta");  // last try to click first video on search results
                    await eval('element.' + f + '(' + args + ')');

                } catch (error) {
                    console.error(error)
                    await process.exit()
                }
            }
        }
    }

    async executeFonction(f: string) {
        try {
            await this.page.waitForFunction(f);
        } catch (error) {
            const url = this.page.url();
            await this.page.goto(url)
            await this.page.waitFor(5000)
            try {
                await this.page.waitForFunction(f);
            } catch (error) {
                console.error(error)
                await process.exit()
            }
        }
    }

    async postConf() {
    }

    async search(): Promise<any> {
    }

    async clickOn(element: any) {
    }

    async clickHome() {
    }

    setRefreshNB(refreshNB: number) {
        this.refreshNB = refreshNB
    }

    // async scrollToEnd(){
    //   let videos = [];
    //   let start = 0;
    //   let end = 500;
    //   let previousWinHeight = -1
    //   let winHeight = (+await this.page.evaluate('document.body.getBoundingClientRect().top')) * -1
    //   while (winHeight > previousWinHeight ) {
    //     await this.page.evaluate('window.scrollTo('+start+', '+end+')')
    //     await this.page.waitFor(1000)
    //     previousWinHeight = winHeight
    //     winHeight = (+await this.page.evaluate('document.body.getBoundingClientRect().top')) * -1
    //     start = end;
    //     end = end + 500;
    //   }
    // }

    async getFullHomepage() {
    }

    async scrollUntil(max_selection: number) {
    }

}
