import fetch from 'node-fetch';

    export async function updateJobStatus(status: string, job_id: number): Promise<number>{
      let args = {status: status};
      let requestHeaders: any = { 'Content-Type': 'application/json' };
      let id;
      console.log(args);

      await fetch('http://192.168.1.13:4000/api/job/'+job_id, {
              method: 'PUT',
              headers: requestHeaders,
              body: JSON.stringify(args)
          }).then((res) => res.json())
          .then((data) =>  id = data['id'])
          .catch((err)=>console.log(err))
      return id;
      // return 0;
    }

    export async function createJob(): Promise<number>{
      let args = {exp_name: 'fetch',date:'date'};
      let requestHeaders: any = { 'Content-Type': 'application/json' };
      let id;
      console.log(args);

      await fetch('http://192.168.1.13:4000/api/jobs', {
              method: 'POST',
              headers: requestHeaders,
              body: JSON.stringify(args)
          }).then((res) => res.json())
          .then((data) =>  id = data['id'])
          .catch((err)=>console.log(err))
      console.log(id);

      return id;
      // return 0;
    }

    export async function saveVideo(video: any, job_id: number): Promise<number>{
      let args = {video, job_id : job_id};
      let requestHeaders: any = { 'Content-Type': 'application/json' };
      let id;
      console.log(args);

      await fetch('http://192.168.1.13:4000/api/videos', {
              method: 'POST',
              headers: requestHeaders,
              body: JSON.stringify(args)
          }).then((res) => res.json())
          .then((data) =>  id = data['id'])
          .catch((err)=>console.log(err))
      return id;
      // return 0;
    }
