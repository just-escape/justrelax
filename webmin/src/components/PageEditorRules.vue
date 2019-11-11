<template>
  <div>
    <div class="row">
      <div class="col">
        Name of the rule
        <div class="container">
          <div class="row">
            <div class="col">
              <div class="text-jaffa">
                <i class="fas fa-exclamation fa-fw"></i> Triggers
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <div class="text-jaffa">
                <i class="fas fa-question fa-fw"></i> Conditions
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <div class="text-jaffa">
                <i class="fas fa-play fa-fw"></i> Actions
              </div>
              <div class="container">
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { SlickList, SlickItem } from 'vue-slicksort'

export default {
  name: 'PageEditorRules',
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
