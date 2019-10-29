<script>
export default {
  name: 'FormValidation',
  data: {
    fieldRefs: []
  },
  methods: {
    onSubmit() {
      for (ref in $data.fieldRefs) {
        console.log(ref)
        this.$refs.ref.validate()
      };
    },
  },
};
</script>