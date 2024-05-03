export class Video {
  private url: string="";
  private title: string = 'title';
  private parent_id: string='';
  private views: string = 'views';
  private depth: number=0;
  private author: string ='author';
  private tags: string[] = [];
  private category: string="";
  private date: string="";
  private duration: string="";
  private subscribers: string="";
  private isFamilyFriendly: string="True";
  private description: string="";
  private paid: string="True";
  private unlisted: string="True";
  private regionAllowed: string[];
  private apiYoutube: string = 'False';
  private homePosition: number= null;
  private refreshNB: number= null;
  private ytkids: string="";
  private bodyHtml: string="";
  private like: string="";
  private dislike: string="";
  private comment: string="";
  private type: string="";
  private insertionDate: Date = new Date();
  private watchTime: number =0;
  private actionNB: number;
  private videoViewsNB: number = 0;

  constructor(url: string, videoViewsNB: number){
    this.url = url;
    this.videoViewsNB = videoViewsNB;
  }

  public setParentId(parent_id: string){
    this.parent_id = parent_id;
  }

  public setType(type: string){
    this.type = type;
  }

  public setTitle(title: string){
    this.title = title;
  }

  public setViews(views: string){
    this.views = views;
  }

  public setAuthor(author: string){
    this.author = author;
  }

  public setTags(tags: string[]){
    this.tags = tags;
  }

  public setCategory(category: string){
    this.category = category;
  }

  public setDate(date: string){
    this.date = date;
  }

  public setDuration(duration: string){
    this.duration = duration;
  }

  public setSubscibers(subscribers: string){
    this.subscribers = subscribers;
  }

  public setIsFamilyFriendly(isFamilyFriendly: string){
    this.isFamilyFriendly = isFamilyFriendly;
  }

  public setDescription(description: string){
    this.description = description;
  }

  public setPaid(paid: string){
    this.paid = paid;
  }

  public setUnlisted(unlisted: string){
    this.unlisted = unlisted;
  }

  public setRegionAllowed(regionAllowed: string[]){
    this.regionAllowed = regionAllowed;
  }

  public setHomePosition(homePosition: number){
    this.homePosition = homePosition;
  }

  public setRefreshNB(refreshNB: number){
    this.refreshNB = refreshNB;
  }

  public setYtkids(ytkids: string){
    this.ytkids = ytkids;
  }

  public setBodyHtml(bodyHtml: string){
    this.bodyHtml = bodyHtml;
  }

  public setLike(like: string){
    this.like = like;
  }

  public setDislike(dislike: string){
    this.dislike = dislike;
  }

  public setWatchTime(watchTime: number){
    this.watchTime = watchTime;
  }

  public setComment(comment: string){
    this.comment = comment;
  }

  public setActionNB(actionNB: number){
    this.actionNB = actionNB;
  }

  public addVideoViews(){
    this.videoViewsNB = this.videoViewsNB + 1;
  }

  public getVideoViewsNB(){
    return this.videoViewsNB;
  }

  public getActionNB(){
    return this.actionNB;
  }
  public getComment(){
    return this.comment;
  }

  public getWatchTime(){
    return this.watchTime;
  }

  public getDislike(){
    return this.dislike;
  }

  public getLike(){
    return this.like;
  }

  public getBodyHtml(){
    return this.bodyHtml;
  }

  public getYtkids(){
    return this.ytkids;
  }

  public getRefreshNB(){
    return this.refreshNB;
  }

  public getHomePosition(){
    return this.homePosition;
  }

  public getRegionAllowed(){
    return this.regionAllowed;
  }

  public getUnlisted(){
    return this.unlisted;
  }

  public getPaid(){
    return this.paid;
  }

  public getDescription(){
    return this.description;
  }

  public getIsFamilyFriendly(){
    return this.isFamilyFriendly;
  }

  public getSubscribers(){
    return this.subscribers;
  }

  public getDuration(){
    return this.duration;
  }

  public getDate(){
    return this.date;
  }

  public getCategory(){
    return this.category;
  }

  public getTags(){
    return this.tags;
  }

  public getAuthor(){
    return this.author;
  }

  public getDepth(){
    return this.depth
  }

  public getParentId(){
    return this.parent_id
  }

  public getTitle(){
    return this.title;
  }

  public getViews(){
    return this.views;
  }

  public getUrl(){
    return this.url;
  }
}
