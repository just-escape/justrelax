<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-play fa-fw"></i> Actions
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="d-flex flex-column">
            <ActionLine
              v-for="a in actions"
              :key="a.index"
              :action="a"
              @updateAction="updateAction"
            />
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
import ActionLine from "@/components/editor/ActionLine.vue"

export default {
  name: 'TabRulesActions',
  components: {
    ActionLine,
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
  methods: {
    updateAction(condition) {
      this.$emit('updateAction', condition)
    },
  },
  props: {
    actions: Array,
  }
}
</script>
