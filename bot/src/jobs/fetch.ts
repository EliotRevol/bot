import {Job} from "./job";
import {Action} from '../abstract/action'
import {YoutubeAction} from '../module/youtube/youtubeAction'

export class Fetch extends Job{

    constructor(page:any, args:any, refreshNB:number, videoViewsNB: number){
      super()
      //console.log("here 95");
      this.action = new YoutubeAction(page,args)
      this.action.setRefreshNB(refreshNB)
      this.action.videoViewsNB = videoViewsNB
      //console.log("here 96");
    }
    async execute(){
      // this.id = await createJob()
      // await this.action.postConf()
      //console.log("executing...");
      this.action.actionNB = this.action.actionNB + 1;
      for (let index = 0; index < this.action.searchSelection; index++) {
        //console.log("doing all this shit");
        await this.action.clickHome()
        await this.action.getFullHomepage()
        this.action.refreshNB = this.action.refreshNB + 1;
      }
      return 0;
    }
}
