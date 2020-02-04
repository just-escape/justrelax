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
              :key="getKey(index)"
              :component="c"
              :context="type"
              :modalId="getModalId(index)"
              :fqdn="getFQDN(index)"
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
    getFQDN() {
      return (index) => {
        var fqdn = JSON.parse(JSON.stringify(this.fqdn))
        fqdn.push(index)
        return fqdn
      }
    },
    getKey() {
      return (index) => {
        return this.getFQDN(index).join('-')
      }
    },
  },
  methods: {
    getModalId(suffix) {
      return this.getFQDN(suffix).join('-')
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
