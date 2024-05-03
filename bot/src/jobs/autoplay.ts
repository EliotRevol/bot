import {Job} from "./job";
import {YoutubeAction} from '../module/youtube/youtubeAction'

export class Autoplay extends Job{

    constructor(page:any,args:any, refreshNB:number, videoViewsNB: number){
      super()
      this.action = new YoutubeAction(page,args)
      this.action.setRefreshNB(refreshNB)
      this.action.videoViewsNB = videoViewsNB
    }
    async execute(){
      const action :YoutubeAction = <YoutubeAction> this.action
      this.action.actionNB = this.action.actionNB + 1;
      for (let index = 1; index < this.action.searchSelection; index++) {
        let autoplay = await action.getAutoplay()
        await this.action.clickOn(autoplay)
      }
      return 0;
    }
}
