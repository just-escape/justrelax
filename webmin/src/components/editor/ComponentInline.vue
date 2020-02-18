<template>
  <div>
    <Template
      :args="args"
      :links="links"
      :templateName="component.template"
      :editable="false"
      class="rounded"
      :class="{'bgc-dark': isSelected}"
      :fqdn="fqdn"
      :modalId="modalId"
    />

    <ComponentModal
      :modalId="modalId"
      :context="context"
      :fqdn="fqdn"
    />

    <div class="container-fluid" v-if="contextParagraphs !== undefined">
      <div class="row">
        <div class="col">
          <ComponentParagraph
            v-for="(cp, index) in contextParagraphs"
            :key="index"
            :title="$t('editor.templates.' + component.template + '.' + cp.key)"
            :context="cp.type"
            :fqdn="getFQDN(cp.key)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Template from '@/components/editor/Template.vue'
import ComponentModal from '@/components/editor/ComponentModal.vue'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ComponentInline",
  components: {
    Template: Template,
    ComponentModal: ComponentModal,
    ComponentParagraph: () => import('@/components/editor/ComponentParagraph.vue'),
  },
  computed: {
    component() {
      return editorStore.getters.dataFromFQDN(this.fqdn)
    },
    links() {
      return editorStore.state.templatesByName[this.component.template].links
    },
    contextParagraphs() {
      return editorStore.state.templatesByName[this.component.template].context_paragraphs
    },
    args() {
      return this.component.arguments
    },
    getFQDN() {
      return (key) => {
        var fqdn = JSON.parse(JSON.stringify(this.fqdn))
        fqdn.push(key)
        return fqdn
      }
    },
    modalId() {
      return this.fqdn.join('-')
    },
    selectedFQDN() {
      return editorStore.state.selectedFQDN
    },
    isSelected() {
      if (this.selectedFQDN === undefined) {
        return false
      } else {
        return this.selectedFQDN.toString() === this.fqdn.toString()
      }
    },
  },
  props: {
    context: String,
    fqdn: Array,
  }
}
</script>
