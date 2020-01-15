<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-fw" :class="icon"></i> {{ title }}
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="d-flex flex-column">
            <ComponentInline
              v-for="(c, index) in components"
              :key="index"
              :component="c"
              :modalId="getModalId(index)"
              :context="type"
              @updateComponent="(c) => updateComponent(index, c)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ComponentInline from "@/components/editor/ComponentInline.vue"

export default {
  name: 'Context',
  components: {
    ComponentInline,
  },
  computed: {
    icon() {
      if (this.type === 'trigger') {
        return ['fa-play']
      } else if (this.type === 'condition') {
        return ['fa-question']
      } else if (this.type === 'action') {
        return ['fa-exclamation']
      } else {
        return []
      }
    },
  },
  methods: {
    getModalId(suffix) {
      return this.type + '-' + suffix
    },
    updateComponent(componentIndex, component) {
      this.$emit('updateComponent', componentIndex, component)
    }
  },
  props: {
    title: String,
    type: String,
    components: Array,
  }
}
</script>
