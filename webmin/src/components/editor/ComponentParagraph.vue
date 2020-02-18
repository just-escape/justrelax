<template>
  <div>
    <div :class="{'text-jaffa': root}">
      <i class="fas fa-fw" :class="icon"></i> {{ title }}
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <draggable :list="storeBoundComponents" :group="{name: context}">
            <ComponentInline
              v-for="(c, index) in storeBoundComponents"
              :key="getKey(index)"
              :context="context"
              :fqdn="getFQDN(index)"
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
  name: 'ComponentParagraph',
  components: {
    draggable,
    ComponentInline,
  },
  computed: {
    icon() {
      if (this.context === 'trigger') {
        return ['fa-play']
      } else if (this.context === 'condition') {
        return ['fa-question']
      } else if (this.context === 'action') {
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
  props: {
    root: {
      type: Boolean,
      default: false,
    },
    title: String,
    context: String,
    fqdn: Array,  // Fully Qualified Data Name
  }
}
</script>
