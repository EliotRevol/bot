import {Job} from "./job";
import {YoutubeAction} from '../module/youtube/youtubeAction'

export class ChannelSniffer extends Job{

    constructor(page:any,args:any, refreshNB:number, videoViewsNB: number){
      super()
      this.action = new YoutubeAction(page,args)
      this.action.setRefreshNB(refreshNB)
      this.action.videoViewsNB = videoViewsNB
    }
    async execute(){
      this.action.actionNB = this.action.actionNB + 1;
      const action :YoutubeAction = <YoutubeAction> this.action
      const videos = await action.searchChannel()
      if (action.getAll) {
        videos.forEach((video:any) => {
          console.log(JSON.stringify(video)+',');

        });
        // console.log('{"videos": '+JSON.stringify(videos)+'},');
        return 0
      }
      for (let index = 0; index < action.searchSelection; index++) {
        const random = Math.floor(Math.random() * videos.length);
        action.searchTerm = videos[random]['title']
        const url = videos[random]['url']
        const video_id = url.substring(url.lastIndexOf('=')+1,url.length)
        action.video_id = video_id
        await this.action.search()
      }

      return 0;
    }
}
