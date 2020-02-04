<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-fw" :class="icon"></i> {{ title }}
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <draggable :list="storeBoundComponents" :group="{name: type}">
            <ComponentInline
              v-for="(c, index) in storeBoundComponents"
              :key="index"
              :component="c"
              :context="type"
              :modalId="getModalId(index)"
              :fqdn="fqdn + [index]"
              @updateComponent="(c) => updateComponent(index, c)"
            />
          </draggable>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ComponentInline from "@/components/editor/ComponentInline.vue"
import editorStore from "@/store/editorStore.js"
import draggable from "vuedraggable"

export default {
  name: 'Context',
  components: {
    draggable,
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
    storeBoundComponents: {
      get() {
        return editorStore.getters.dataFromFQDN(this.fqdn)
      },
      set(value) {
        let fqdn = this.fqdn
        let data = value
        editorStore.commit('setDataFromFQDN', {fqdn, data})
      },
    },
  },
  methods: {
    getModalId(suffix) {
      return this.fqdn + '-' + suffix
    },
    updateComponent(componentIndex, component) {
      this.$emit('updateComponent', componentIndex, component)
    }
  },
  props: {
    title: String,
    type: String,
    fqdn: Array,  // Fully Qualified Data Name
  }
}
</script>
