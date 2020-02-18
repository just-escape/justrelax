<template>
  <div>
    <div
      class="rounded"
      :class="{'bgc-dark': selectedFQDN === fqdn}"
      @click="paragraphClicked()"
    >
      <span :class="{'text-jaffa': root}">
        <i class="mr-1 fas fa-fw" :class="icon"></i>{{ title }}
      </span>
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <draggable
            @start="onDragStart"
            @update="onDragUpdate"
            @end="onDragUpdate"
            handle=".handle"
            :list="storeBoundComponents"
            :group="{name: context}"
          >
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
      return [editorStore.getters.iconFromContext(this.context)]
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
    selectedFQDN() {
      return editorStore.state.selectedFQDN
    },
  },
  methods: {
    paragraphClicked() {
      editorStore.commit('setSelectedFQDN', this.fqdn)
    },
    onDragStart(event) {
      var fqdn = JSON.parse(JSON.stringify(this.fqdn))
      fqdn.push(event.oldIndex)
      editorStore.commit('setSelectedFQDN', fqdn)
    },
    onDragUpdate(event) {
      var fqdn = JSON.parse(JSON.stringify(this.fqdn))
      fqdn.push(event.newIndex)
      editorStore.commit('setSelectedFQDN', fqdn)
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
