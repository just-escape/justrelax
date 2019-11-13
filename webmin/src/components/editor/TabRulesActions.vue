<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-play fa-fw"></i> Actions
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="d-flex flex-column">
            <Action v-for="a in actions" :key="a.index" :action="a"/>
          </div>
          <!--<SlickList v-model="items">
            <SlickItem
              v-for="(item, index) in items"
              :index="index"
              :key="index"
            >
              {{ item }}
            </SlickItem>
          </SlickList>-->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { SlickList, SlickItem } from 'vue-slicksort'
import Action from "@/components/editor/Action.vue"

export default {
  name: 'TabRulesActions',
  components: {
    Action,
  },
  /*components: {
    SlickList,
    SlickItem,
  },
  data() {
    return {
      items: [1, 2, 3]
    }
  },*/
  props: {
    actions: Array,
  }
}
</script>
