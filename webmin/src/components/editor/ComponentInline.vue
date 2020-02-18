<template>
  <div>
    <Template
      v-b-modal="modalId"
      class="pointer"
      :args="args"
      :links="links"
      :templateName="component.template"
    />

    <ComponentModal
      :modalId="modalId"
      :context="context"
      :fqdn="fqdn"
    />

    <div class="container-fluid" v-if="component.template === 'if_then_else_multiple_functions'">
      <div class="row">
        <div class="col">
          <SubContextParagraph
            :title="$t('editor.if_conditions')"
            context="condition"
            :fqdn="getFQDN('if_conditions')"
          />
          <SubContextParagraph
            :title="$t('editor.then_actions')"
            context="action"
            :fqdn="getFQDN('then_actions')"
          />
          <SubContext
            :title="$t('editor.else_actions')"
            context="action"
            :fqdn="getFQDN('else_actions')"
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
    SubContextParagraph: () => import('@/components/editor/Context.vue'),
  },
  computed: {
    component() {
      return editorStore.getters.dataFromFQDN(this.fqdn)
    },
    links() {
      return editorStore.state.templatesByName[this.component.template].links
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
  },
  props: {
    context: String,
    fqdn: Array,
  }
}
</script>
