<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-play fa-fw"></i> Actions
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <SlickList v-model="items">
            <SlickItem
              v-for="(item, index) in items"
              :index="index"
              :key="index"
            >
              {{ item }}
            </SlickItem>
          </SlickList>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { SlickList, SlickItem } from 'vue-slicksort'

export default {
  name: 'TabRulesActions',
  components: {
    SlickList,
    SlickItem,
  },
  data() {
    return {
      items: [1, 2, 3]
    }
  }
}
</script>
