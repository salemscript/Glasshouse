/* Optimistic per-item sync. Concurrent edits are kept for the learner to resolve. */
window.GlasshouseAccountSync = function(client,store,notify=()=>{}) {
  let owner=null,busy=false,generation=0;const conflicts=new Map();
  function setUser(id){owner=id;generation++;busy=false;conflicts.clear();}
  async function sync(){
    if(!owner||busy)return;const id=owner,turn=generation;busy=true;let changed=false;
    const current=()=>turn===generation&&id===owner;
    notify({state:'saving'});
    try{
      for(let offset=0;;offset+=500){
        const {data,error}=await client.from('learning_items').select('key,value,version').eq('user_id',id).order('key').range(offset,offset+499);
        if(error)throw error;if(!current())return;
        for(const item of data){if(!store.allowed(item.key))continue;const local=store.row(id,item.key);
          if(local?.dirty&&local.revision!==item.version){if(local.value===item.value){store.acknowledge(id,item.key,local,item.version);conflicts.delete(item.key);}else conflicts.set(item.key,item);}
          else changed=store.receive(id,item.key,item.value,item.version)||changed;
        }
        if(data.length<500)break;
      }
      for(const key of store.keys(id)){
        if(!current())return;const local=store.row(id,key);if(!local?.dirty||conflicts.has(key))continue;
        const {data,error}=await client.rpc('save_learning_item',{p_owner_id:id,p_key:key,p_value:local.value,p_expected_version:local.revision});
        if(error)throw error;if(!current())return;
        if(data.conflict)conflicts.set(key,data.item);else store.acknowledge(id,key,local,data.item.version);
      }
      if(current())notify({state:conflicts.size?'conflict':store.keys(id).some(k=>store.row(id,k)?.dirty)?'pending':'saved',changed,conflicts:[...conflicts.values()]});
    }catch{if(current())notify({state:'offline',changed});}
    finally{if(current())busy=false;}
  }
  function resolve(key,keepLocal){const remote=conflicts.get(key);if(!owner||!remote)return;store.resolve(owner,key,remote,keepLocal);conflicts.delete(key);return sync();}
  return {setUser,sync,resolve,pending:()=>owner&&store.keys(owner).some(k=>store.row(owner,k)?.dirty),conflicts:()=>[...conflicts.values()]};
};
