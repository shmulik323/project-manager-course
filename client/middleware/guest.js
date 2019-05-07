export default function ({
  store,
  redirect
}) {
  // If the user is authenticated redirect to home page
  if (store.auth) {
    return redirect('/')
  }
}
