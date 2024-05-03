import {Job} from "./job";
import {YoutubeAction} from '../module/youtube/youtubeAction'

export class WatchOne extends Job{

    constructor(page:any,args:any, refreshNB:number, videoViewsNB: number){
      super()
      this.action = new YoutubeAction(page,args)
      this.action.setRefreshNB(refreshNB)
      this.action.videoViewsNB = videoViewsNB
    }
    async execute(){
      this.action.actionNB = this.action.actionNB + 1;
      await this.action.search()
      return 0;
    }
}
