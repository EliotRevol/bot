import {Job} from "./job";
import {YoutubeAction} from '../module/youtube/youtubeAction'

export class FetchAutoplay extends Job{

    constructor(page:any,args:any, refreshNB:number, videoViewsNB: number){
      super()
      this.action = new YoutubeAction(page,args)
      this.action.setRefreshNB(refreshNB)
      this.action.videoViewsNB = videoViewsNB
    }
    async execute(){
      const action :YoutubeAction = <YoutubeAction> this.action
      for (let index = 1; index < this.action.searchSelection; index++) {
        await action.fillAutoplaysearch()
        await this.action.clickHome()
        this.action.actionNB = this.action.actionNB + 1;
        await this.action.getFullHomepage()
        this.action.refreshNB = this.action.refreshNB + 1;
        this.action.actionNB = this.action.actionNB + 1;
        await this.action.search()
      }
      return 0;
    }
}
